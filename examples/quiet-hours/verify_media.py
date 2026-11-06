#!/usr/bin/env python3
"""Verify a rendered Quiet Hours project and optionally rerender one retake."""

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from studio.render import (  # noqa: E402
    FORMAT_SIZES,
    RenderCancelled,
    _picture_delta,
    reference_html,
    render_campaign,
)
from studio.server import StudioServer  # noqa: E402
from studio.store import Store  # noqa: E402


def rgb_frame(file, seconds):
    return subprocess.check_output(
        [
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-ss",
            f"{seconds:.3f}",
            "-i",
            file,
            "-vf",
            "scale=270:-2",
            "-frames:v",
            "1",
            "-pix_fmt",
            "rgb24",
            "-f",
            "rawvideo",
            "pipe:1",
        ],
        timeout=10,
    )


def color_count(pixels, predicate):
    return sum(predicate(*color) for color in zip(pixels[0::3], pixels[1::3], pixels[2::3]))


def check_pixels(file):
    checks = {}
    for seconds in (0, 2.9, 5.6, 8.6, 9.6, 12.5):
        frame = rgb_frame(file, seconds)
        planning = color_count(frame, lambda r, g, b: r > 190 and g < 80 and b > 140)
        if planning:
            raise ValueError(f"Planning-only marker appears at {seconds:g}s")
        checks[f"planning-marker-{seconds:g}s"] = planning
    packshot = rgb_frame(file, 5.6)
    sticker = color_count(packshot, lambda r, g, b: 140 < r < 235 and g > 195 and b < 110)
    clip = rgb_frame(file, 8.6)
    lavender = color_count(clip, lambda r, g, b: 217 < r < 239 and 206 < g < 233 and b > 244)
    if sticker < 25 or lavender < 500:
        raise ValueError("Decoded picture is missing the imported artwork or clip")
    return {**checks, "importedPackshotLimePixels": sticker, "importedClipLavenderPixels": lavender}


def browser_evidence(store, state, out):
    files = {key: store.file_path(state, f"master-{key}.mp4") for key in FORMAT_SIZES}
    root = f"/api/projects/{state['id']}"
    samples = {"9x16": [0, 2.9, 5.6, 8.6, 9.6, 12.5], "1x1": [0, 9.6], "16x9": [0, 12.5]}
    with StudioServer(0, store) as server, tempfile.TemporaryDirectory(dir=out) as directory:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            work = Path(directory)
            frames = [
                {
                    "format": ratio,
                    "time": seconds,
                    "route": f"{root}/preview?time={seconds}&format={ratio}",
                    "file": str(work / f"{ratio}-{seconds}.png"),
                    "width": FORMAT_SIZES[ratio][0],
                    "height": FORMAT_SIZES[ratio][1],
                }
                for ratio, times in samples.items()
                for seconds in times
            ]
            manifest = {
                "origin": f"http://{server.host}",
                "frames": frames,
                "clips": [
                    {"format": ratio, "route": f"{root}/files/master-{ratio}.mp4"} for ratio in FORMAT_SIZES
                ],
                "result": str(work / "browser.json"),
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest))
            subprocess.run(["node", HERE / "capture_media.mjs", manifest_path], check=True, timeout=110)
            playback = json.loads((work / "browser.json").read_text())
            comparisons = [
                {
                    "format": frame["format"],
                    "time": frame["time"],
                    "browserToDecodedSsim": _picture_delta(
                        frame["file"], files[frame["format"]], frame["time"], work, lambda: False
                    ),
                }
                for frame in frames
            ]
            return {
                "pixelChecks": check_pixels(files["9x16"]),
                "browserPreviewAgreement": comparisons,
                "browserPlayback": playback,
            }
        finally:
            server.shutdown()
            thread.join(timeout=5)


def retake(store, state, out):
    # Restore the authored local picture to make a starting-frame handoff.
    shot = next(shot for shot in state["shots"] if shot["id"] == "stamp")
    local = {**shot, "asset": "", "trimMs": 0}
    local_scene = {**state, "shots": [local if s["id"] == shot["id"] else s for s in state["shots"]]}
    assets = store.path(state["id"], "assets")
    reference = reference_html(local_scene, "stamp", assets)
    (out / "stamp-reference.html").write_text(reference)
    if "Planning reference" not in reference or "Keys land" not in reference:
        raise ValueError("The clip handoff lost planning or action instructions")
    clip = store.asset_path(state, shot["asset"])
    retake_clip = out / "key-drop-retake.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-i",
            clip,
            "-vf",
            "eq=brightness=0.035",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            "-y",
            retake_clip,
        ],
        check=True,
        timeout=25,
    )
    revision = state["revision"]
    changed = store.change(
        state["id"],
        revision,
        "import",
        {
            "name": "key-drop-retake.mp4",
            "role": "clip",
            "rights": "Original Quiet Hours demo derivative, MIT.",
            "source": "Local retake. Brightness raised 0.035 in the original motion clip.",
            "disclosure": "Original synthetic demo material.",
            "consent": "",
            "data": base64.b64encode(retake_clip.read_bytes()).decode(),
        },
    )
    replacement = changed["assets"][-1]
    changed = store.change(
        state["id"],
        changed["revision"],
        "storyboard",
        {
            "shots": [
                {**item, "asset": replacement["id"]} if item["id"] == shot["id"] else item
                for item in state["shots"]
            ],
            "hooks": state["hooks"],
            "selectedHook": state["selectedHook"],
            "tracks": state["tracks"],
            "cuts": state["cuts"],
        },
    )
    cache = store.path(state["id"], "cache")
    render = render_campaign(changed, assets, out / "retake", cache)
    if (
        render["stats"]["pictureRendered"] != 3
        or render["stats"]["pictureCacheHits"] != 12
        or not render["stats"]["audioCacheHit"]
    ):
        raise ValueError("Retake did not reuse all unchanged shots and audio")
    requested = time.monotonic()
    try:
        render_campaign(
            changed,
            assets,
            out / "cancelled",
            cache,
            cancelled=lambda: time.monotonic() - requested > 0.55,
        )
    except RenderCancelled:
        if (out / "cancelled").exists() or list(out.glob(".render-*")):
            raise ValueError("Cancelled render left unpublished output")
    else:
        raise ValueError("Expected an in-flight cancellation")
    return {
        "stableShot": shot["id"],
        "initialRevision": revision,
        "retakeRevision": changed["revision"],
        "approvalAfterEdit": changed["approval"],
        "sourceClipChanged": shot["asset"] != replacement["id"],
        "handoffSelfContained": "data:image/png;base64," in reference,
        "handoffSha256": hashlib.sha256(reference.encode()).hexdigest(),
        "render": render["stats"],
        "inFlightCancellationCleaned": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--project", default="quiet-hours")
    parser.add_argument("--retake", action="store_true", help="Persist a test retake in disposable storage")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    store = Store(args.data)
    state = store.get(args.project, raw=True)
    if not state["demo"] or not state["render"]:
        raise ValueError("Render the fictional demo before running media verification")
    evidence = browser_evidence(store, state, args.output)
    if args.retake:
        evidence["retake"] = retake(store, state, args.output)
    (args.output / "verification.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
