"""Trusted scene composition, shot cache, and media delivery."""

import base64
import hashlib
import json
import math
import os
import re
import shutil
import signal
import struct
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape
from pathlib import Path
from threading import Event

from .scene_art import illustration

ROOT = Path(__file__).resolve().parent.parent
NODE = ROOT / "node_modules"
HYPERFRAMES = NODE / "hyperframes" / "bin" / "hyperframes.mjs"
GSAP = NODE / "gsap" / "dist" / "gsap.min.js"
FONT = NODE / "@fontsource" / "space-grotesk" / "files" / "space-grotesk-latin-700-normal.woff2"
CSS = Path(__file__).with_name("scene.css").read_text(encoding="utf-8")
FPS = 30
# Stable picture contract revision. Bump when scene geometry, timing, or encoding changes.
PICTURE_CONTRACT_REVISION = "7d39ef30bfa8b800eed6f0afacbc059712c101136f48c6218167272c822906da"
AUDIO_MIX_VERSION = 2
AUDIO_LOUDNORM = "loudnorm=I=-14:TP=-2.3:LRA=9"
FORMAT_SIZES = {"9x16": (1080, 1920), "1x1": (1080, 1080), "16x9": (1920, 1080)}
PICTURE_ROLES = {"packshot", "logo", "background", "cutout", "clip"}
AUDIO_ROLES = {"voice", "music", "foley"}
EXTENSIONS = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
}
PALETTES = {
    "citation": ("#f48072", "#171628", "#f5a096", "#171628"),
    "clipboard": ("#fff6e2", "#171628", "#e2ddf5", "#171628"),
    "packshot": ("#263eb5", "#fff6e2", "#d5dbfa", "#171628"),
    "stamp": ("#f2c643", "#171628", "#ffdd62", "#171628"),
    "end": ("#171628", "#fff6e2", "#e2ddf5", "#171628"),
}
MOTIONS = {
    "citation": ((0, 0, 0.98), (0, 0, 1), 0.65),
    "clipboard": ((-80, 0, 1), (0, 0, 1), 0.55),
    "packshot": ((0, 10, 0.91), (0, 0, 1), 0.62),
    "stamp": ((0, 12, 1), (0, 0, 1), 0.36),
    "end": ((0, 0, 1), (0, 0, 1), 0.28),
    "still": ((0, 0, 1), (0, 0, 1), 0.28),
    "push": ((0, 0, 0.9), (0, 0, 1), 1.1),
    "float": ((0, 44, 1), (0, 0, 1), 0.7),
}


class PreviewError(ValueError):
    """A timestamp, format, or reference is unavailable."""


class RenderError(ValueError):
    """A media input or renderer command did not pass its checks."""


class RenderCancelled(RenderError):
    """The current render was cancelled without publishing outputs."""


def _seconds(ms):
    return f"{ms / 1000:.6f}"


def _safe_asset_id(value):
    return isinstance(value, str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", value)


def _asset(state, asset_id, roles):
    if not asset_id:
        return None
    return next(
        (asset for asset in state["assets"] if asset["id"] == asset_id and asset["role"] in roles),
        None,
    )


def _asset_file(asset_dir, asset):
    if not _safe_asset_id(asset["id"]) or asset.get("ext") not in EXTENSIONS:
        raise RenderError("Invalid media identity")
    file = asset_dir / (asset["id"] + asset["ext"])
    if asset_dir.is_symlink() or file.is_symlink() or not file.is_file():
        raise RenderError("Media file missing or outside managed storage")
    if asset.get("sha256") and _sha(file) != asset["sha256"]:
        raise RenderError("Stored media bytes changed. Import a new asset revision.")
    return file


def _hook_title(state, shot, hook):
    if shot["beat"] != "hook" or not hook:
        return shot["title"]
    for option in state["hooks"]:
        if option["id"] == hook:
            return option["title"]
    raise PreviewError("Unknown hook")


def _layout(ratio, title):
    # The vertical words and foreground stay within x=108..972, y=168..1330.
    longest = max((len(word) for word in title.split()), default=1)
    if ratio == "16x9":
        width = 676
        size = min(126, max(55, 150 - 1.35 * len(title)), width / (longest * 0.64))
        return f"""
.folio{{left:150px;right:150px;top:101px}}
.rule{{left:150px;right:150px;top:150px}}
.bottom-rule{{left:150px;right:150px;top:939px}}
.copy{{left:150px;top:285px;width:{width}px}}
.headline{{font-size:{max(35, size):.2f}px}}
.art{{left:890px;top:220px;width:880px;height:625px}}
.caption{{left:150px;top:755px;max-width:{width}px}}
"""
    if ratio == "1x1":
        width = 880
        size = min(105, max(56, 124 - 1.15 * len(title)), width / (longest * 0.64))
        return f"""
.folio{{left:100px;right:100px;top:78px}}
.rule{{left:100px;right:100px;top:119px}}
.bottom-rule{{left:100px;right:100px;top:1002px}}
.copy{{left:100px;top:148px;width:{width}px}}
.headline{{font-size:{max(35, size):.2f}px}}
.art{{left:100px;top:390px;width:880px;height:475px}}
.caption{{left:100px;top:895px;max-width:{width}px}}
"""
    width = 864
    size = min(129, max(68, 151 - 1.25 * len(title)), width / (longest * 0.64))
    return f"""
.folio{{left:108px;right:108px;top:184px}}
.rule{{left:108px;right:108px;top:233px}}
.bottom-rule{{left:108px;right:108px;top:1432px}}
.copy{{left:108px;top:283px;width:{width}px}}
.headline{{font-size:{max(35, size):.2f}px}}
.art{{left:108px;top:579px;width:864px;height:589px}}
.caption{{left:108px;top:1203px;max-width:{width}px}}
"""


def _motion(shot):
    style = shot.get("style", "citation")
    return MOTIONS.get(shot.get("motion"), MOTIONS.get(style, MOTIONS["still"]))


def _pose(shot, time_ms):
    start, end, duration = _motion(shot)
    t = min(1, max(0, time_ms / (duration * 1000)))
    eased = 1 - (1 - t) ** 4
    x, y, scale = [a + (b - a) * eased for a, b in zip(start, end)]
    return f"translate({x:.5f}px,{y:.5f}px) scale({scale:.8f})"


def _reveal_ms(state, shot):
    # The fictional key lands about one second into the authored clip.
    if state.get("demo") and shot["id"] == "stamp" and shot["durationMs"] >= 3000:
        return 1133
    return 0


def _scene(state, shot, ratio, duration, asset_src, *, hook, captions, preview_ms=None):
    style = shot.get("style", "citation")
    paper, ink, panel, panel_ink = PALETTES.get(style, PALETTES["citation"])
    title = _hook_title(state, shot, hook)
    label = escape(shot["beat"].replace("-", " ").upper())
    brand = escape(state["brief"].get("brand", ""))
    layout = _layout(ratio, title)
    subtitle = escape(shot.get("caption", "")).replace("\n", "<br>")
    duration_s = _seconds(duration)
    trim_s = _seconds(shot.get("trimMs", 0))
    asset = _asset(state, shot.get("asset"), PICTURE_ROLES)
    source = asset_src(asset) if asset else None
    art = illustration(style)
    backdrop = ""
    if source:
        source = escape(source, quote=True)
        if asset["role"] == "clip":
            art = (
                f'<video id="placed-video" class="clip placed-video" src="{source}" '
                f'data-start="0" data-duration="{duration_s}" data-track-index="0" '
                f'data-media-start="{trim_s}" data-volume="0" muted playsinline preload="auto"></video>'
            )
        elif asset["role"] == "background":
            backdrop = f'<img class="backdrop" src="{source}" alt="">'
        else:
            art = f'<img class="placed-image" src="{source}" alt="">'
    pose = f' style="transform:{_pose(shot, preview_ms)}"' if preview_ms is not None else ""
    reveal_ms = _reveal_ms(state, shot)
    reveal_class, reveal_style = "", ""
    if reveal_ms:
        reveal_class = " stamp-reveal"
        opacity = max(0, min(1, ((preview_ms or 0) - reveal_ms) / 120))
        reveal_style = f' style="opacity:{opacity:.5f}"'
    caption = (
        f'<p class="caption{reveal_class}"{reveal_style}>{subtitle}</p>' if captions and subtitle else ""
    )
    width, height = FORMAT_SIZES[ratio]
    return f"""
<style>{CSS}{layout}</style>
<div id="root" class="scene" data-composition-id="shot" data-width="{width}" data-height="{height}"
  style="--paper:{paper};--ink:{ink};--panel:{panel};--panel-ink:{panel_ink}">
  <div class="surface" aria-hidden="true">{backdrop}</div>
  <div class="folio"><b>{brand}</b><span>{label}</span></div>
  <div class="rule" aria-hidden="true"></div>
  <div class="copy{reveal_class}"{reveal_style}>
    <div class="kicker">{escape(state["brief"].get("product", ""))}</div>
    <h1 class="headline">{escape(title)}</h1>
  </div>
  <div class="art"><div id="art-visual" class="art-visual"{pose}>{art}</div></div>
  {caption}
  <div class="bottom-rule" aria-hidden="true"></div>
</div>
"""


def _preview_font():
    if not FONT.is_file():
        return ""
    encoded = base64.b64encode(FONT.read_bytes()).decode("ascii")
    return f"@font-face{{font-family:StudioSpace;src:url(data:font/woff2;base64,{encoded});font-weight:700}}"


def _preview_document(content, width, height, video_seek, embedded):
    script = (
        ""
        if embedded
        else f"""<script>

const fit = document.getElementById("fit");
function resize() {{
  const factor = Math.min(innerWidth / {width}, innerHeight / {height});
  fit.style.left = ((innerWidth - {width} * factor) / 2) + "px";
  fit.style.top = ((innerHeight - {height} * factor) / 2) + "px";
  fit.style.transform = "scale(" + factor + ")";
}}
addEventListener("resize", resize);
resize();
const media = document.getElementById("placed-video");
if (media) {{
  const seek = () => {{ media.currentTime = Math.min({video_seek}, media.duration); }};
  if (media.readyState) seek(); else media.addEventListener("loadedmetadata", seek, {{once:true}});
}}
</script>"""
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width={width},initial-scale=1">
<title>Storyboard preview</title>
<style>{_preview_font()}
html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#171628}}
#fit{{position:absolute;width:{width}px;height:{height}px;transform-origin:top left}}
</style></head><body>
<main id="fit" data-media-seek="{video_seek}">{content}</main>{script}</body></html>"""


def preview_html(state, time_ms, ratio="9x16", hook=None, media_url=None, *, captions=True, embedded=False):
    """Render the selected storyboard frame into a responsive iframe document."""
    if ratio not in FORMAT_SIZES:
        raise PreviewError("Unknown aspect ratio")
    if not isinstance(time_ms, (int, float)) or not math.isfinite(time_ms) or time_ms < 0:
        raise PreviewError("Invalid timestamp")
    total = sum(shot["durationMs"] for shot in state["shots"])
    if not total or time_ms > total:
        raise PreviewError("Timestamp is outside the storyboard")
    time_ms = min(total - 0.001, time_ms)

    def source(asset):
        if not media_url or not _safe_asset_id(asset["id"]):
            return None
        url = media_url(asset["id"])
        if not isinstance(url, str) or not re.fullmatch(r"/[A-Za-z0-9_/.-]+(?:\?preview=[0-9a-f]{64})?", url):
            raise PreviewError("Preview media must be a local URL")
        if url.startswith("//"):
            raise PreviewError("Preview media must be a local URL")
        return url

    for shot in state["shots"]:
        duration = shot["durationMs"]
        if time_ms < duration:
            content = _scene(
                state,
                shot,
                ratio,
                duration,
                source,
                hook=hook or state.get("selectedHook"),
                captions=captions,
                preview_ms=time_ms,
            )
            seek = _seconds(shot.get("trimMs", 0) + time_ms)
            return _preview_document(content, *FORMAT_SIZES[ratio], seek, embedded)
        time_ms -= duration
    raise PreviewError("Timestamp is outside the storyboard")


def reference_html(state, shot_id, asset_dir):
    """A local, self-contained handoff with artwork and production instructions."""
    shot = next((shot for shot in state["shots"] if shot["id"] == shot_id), None)
    if shot is None:
        raise PreviewError("Shot is unavailable")
    asset_dir = Path(asset_dir)

    def source(asset):
        mime = EXTENSIONS.get(asset.get("ext"), "")
        if not mime.startswith("image/"):
            return None
        data = base64.b64encode(_asset_file(asset_dir, asset).read_bytes()).decode("ascii")
        return f"data:{mime};base64,{data}"

    content = _scene(
        state,
        shot,
        "9x16",
        shot["durationMs"],
        source,
        hook=state.get("selectedHook"),
        captions=True,
        preview_ms=0,
    )
    reference = _asset(state, shot.get("reference"), {"reference"})
    reference_src = source(reference) if reference else None
    reference_img = (
        f'<h2>Planning reference</h2><img class="reference" src="{reference_src}" alt="Planning reference">'
        if reference_src
        else ""
    )
    name = escape(shot["id"])
    action = escape(shot["action"])
    rights = escape(state["brief"].get("rights", ""))
    audio = escape(shot.get("audio", ""))
    evidence = escape(shot.get("evidence", ""))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shot handoff · {name}</title>
<style>{_preview_font()}
body{{font:16px/1.5 system-ui;background:#fff6e2;color:#171628;max-width:980px;margin:2rem auto;padding:0 1rem}}
.ref-sheet{{display:flex;align-items:start;gap:2rem;flex-wrap:wrap}}
.frame{{position:relative;overflow:hidden;width:270px;height:480px}}
.frame > div{{width:1080px;height:1920px;transform:scale(.25);transform-origin:top left}}
.notes{{max-width:560px}}.reference{{max-width:100%;max-height:440px}}
</style></head><body><h1>Shot handoff · {name}</h1>
<div class="ref-sheet"><div><h2>Editable starting frame</h2><div class="frame"><div>{content}</div></div></div>
<div class="notes"><h2>Shot prompt</h2><p>{action}</p>
<p>Duration {_seconds(shot["durationMs"])}s · 9:16 · 1080 × 1920 · 30 fps</p>
<p>Keep approved product appearance, colors, framing, and claim wording. Preserve any source
watermark and attach usage rights, disclosures, and consent before import.</p>
<p><strong>Audio cue</strong> {audio}</p><p><strong>Evidence</strong> {evidence}</p>
<p><strong>Rights context</strong> {rights}</p>{reference_img}</div></div></body></html>"""


def _srt_time(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"


def srt_captions(state):
    cursor = 0
    lines = []
    for shot in state["shots"]:
        stop = cursor + shot["durationMs"]
        caption = shot.get("caption", "").strip()
        if caption:
            lines.append(
                f"{len(lines) + 1}\n{_srt_time(cursor + _reveal_ms(state, shot))} --> {_srt_time(stop)}\n{escape(caption)}"
            )
        cursor = stop
    return "\n\n".join(lines) + ("\n" if lines else "")


def _run(args, *, cwd=None, env=None, cancelled=lambda: False, timeout=240):
    _check_cancel(cancelled)
    started = time.monotonic()
    with tempfile.TemporaryFile() as output:
        try:
            process = subprocess.Popen(
                [str(a) for a in args],
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=output,
                stderr=subprocess.STDOUT,
                start_new_session=os.name == "posix",
            )
        except OSError as error:
            raise RenderError(f"Unable to start {Path(args[0]).name}") from error
        try:
            while process.poll() is None:
                _check_cancel(cancelled)
                if time.monotonic() - started > timeout:
                    raise RenderError(f"{Path(args[0]).name} timed out")
                time.sleep(0.06)
        except BaseException:
            if process.poll() is None:
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    process.kill()
            process.wait()
            raise
        output.seek(max(0, output.tell() - 128_000))
        result = output.read().decode("utf-8", "replace")
        if process.returncode:
            if os.environ.get("STUDIO_RENDER_DEBUG") == "1":
                print(result, flush=True)
            command = (
                "HyperFrames " + str(args[2])
                if len(args) > 2 and args[1] == HYPERFRAMES
                else Path(args[0]).name
            )
            raise RenderError(f"{command} exited with status {process.returncode}")
        return result


def _check_cancel(cancelled):
    if cancelled():
        raise RenderCancelled("Render cancelled")


def _ffmpeg(args, cancelled, timeout=180):
    return _run(["ffmpeg", "-nostdin", "-hide_banner", *args], cancelled=cancelled, timeout=timeout)


def _probe(file, cancelled):
    result = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-protocol_whitelist",
            "file,pipe",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            file,
        ],
        cancelled=cancelled,
        timeout=20,
    )
    return json.loads(result)


def _inspect_video(file, ratio, frames, cancelled, *, audio=False, decode=False):
    data = _probe(file, cancelled)
    stream = next((s for s in data["streams"] if s["codec_type"] == "video"), {})
    sound = next((s for s in data["streams"] if s["codec_type"] == "audio"), {})
    dimensions = stream.get("width"), stream.get("height")
    rate = stream.get("r_frame_rate", "0/1")
    duration = float(stream.get("duration", "0"))
    if (
        dimensions != FORMAT_SIZES[ratio]
        or stream.get("codec_name") != "h264"
        or rate != f"{FPS}/1"
        or int(stream.get("nb_frames", 0)) != frames
        or abs(duration - frames / FPS) > 0.04
        or (audio and sound.get("codec_name") != "aac")
    ):
        raise RenderError(f"{ratio} media metadata does not match the render contract")
    if decode:
        _ffmpeg(["-v", "error", "-xerror", "-i", file, "-f", "null", "-"], cancelled)
    return {
        "width": dimensions[0],
        "height": dimensions[1],
        "frames": frames,
        "fps": FPS,
        "duration": round(duration, 3),
        "codec": stream["codec_name"],
        "audio": sound.get("codec_name"),
        "decoded": decode,
    }


def _sha(file):
    with Path(file).open("rb") as data:
        return hashlib.file_digest(data, "sha256").hexdigest()


def _installed():
    if not all(path.is_file() for path in (HYPERFRAMES, GSAP, FONT)):
        raise RenderError("Run npm ci to install the locked renderer, GSAP, and font")


def _project(work, state, shot, ratio, frames, asset):
    duration = frames * 1000 / FPS
    width, height = FORMAT_SIZES[ratio]
    assets = work / "assets"
    assets.mkdir()
    shutil.copyfile(GSAP, assets / "gsap.min.js")
    shutil.copyfile(FONT, assets / "studio-space.woff2")
    source = None
    if asset:
        asset_path, name = asset
        source = "assets/source" + name["ext"]
        shutil.copyfile(asset_path, work / source)
    content = _scene(
        state,
        shot,
        ratio,
        duration,
        lambda _asset: source,
        hook=state.get("selectedHook"),
        captions=True,
    )
    start, end, move_duration = _motion(shot)
    initial = json.dumps(dict(zip(("x", "y", "scale"), start)))
    final = json.dumps(
        {**dict(zip(("x", "y", "scale"), end)), "duration": move_duration, "ease": "power4.out"}
    )
    reveal_ms = _reveal_ms(state, shot)
    reveal = (
        'motion.fromTo(".stamp-reveal", {opacity:0}, '
        '{opacity:1,duration:0.12,ease:"none"}, ' + _seconds(reveal_ms) + ");"
        if reveal_ms
        else ""
    )
    (work / "compositions").mkdir()
    (work / "compositions" / "shot.html").write_text(
        f"""<template>{content}
<script>
const motion = gsap.timeline({{paused:true}});
motion.fromTo("#art-visual", {initial}, {final}, 0);
{reveal}
window.__timelines["shot"] = motion;
</script></template>""",
        encoding="utf-8",
    )
    duration_s = _seconds(duration)
    (work / "index.html").write_text(
        f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Studio composition</title>
<script src="assets/gsap.min.js"></script><style>
@font-face{{font-family:StudioSpace;src:url(assets/studio-space.woff2);font-weight:700}}
html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:#171628}}
#main,#shot{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}
</style></head><body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{duration_s}"
 data-width="{width}" data-height="{height}" data-fps="{FPS}">
 <div id="shot" data-composition-id="shot" data-composition-src="compositions/shot.html"
  data-start="0" data-duration="{duration_s}" data-track-index="0"
  data-width="{width}" data-height="{height}"></div>
</div>
<script>window.__timelines = {{main:gsap.timeline({{paused:true}})}};</script></body></html>""",
        encoding="utf-8",
    )


def _hyperframes_env(work):
    # No provider credentials are needed by the local renderer.
    allow = (
        "PATH",
        "HOME",
        "USERPROFILE",
        "SystemRoot",
        "LANG",
        "LC_ALL",
        "PUPPETEER_CACHE_DIR",
        "PUPPETEER_EXECUTABLE_PATH",
        "CHROME_PATH",
    )
    env = {key: os.environ[key] for key in allow if key in os.environ}
    return {
        **env,
        "TMPDIR": str(work),
        "TEMP": str(work),
        "TMP": str(work),
        "HYPERFRAMES_NO_TELEMETRY": "1",
        "DO_NOT_TRACK": "1",
    }


def _snapshot_size(file):
    with file.open("rb") as data:
        header = data.read(24)
    if not header.startswith(b"\x89PNG\r\n\x1a\n") or len(header) != 24:
        raise RenderError("Invalid HyperFrames snapshot")
    return struct.unpack(">II", header[16:24])


def _check_snapshot(file, ratio, cancelled):
    if _snapshot_size(file) != FORMAT_SIZES[ratio]:
        raise RenderError("HyperFrames snapshot dimensions do not match")
    result = _ffmpeg(
        [
            "-v",
            "info",
            "-i",
            file,
            "-vf",
            "scale=96:96,signalstats,metadata=print",
            "-frames:v",
            "1",
            "-f",
            "null",
            "-",
        ],
        cancelled,
    )
    low = re.search(r"lavfi\.signalstats\.YLOW=(\d+)", result)
    high = re.search(r"lavfi\.signalstats\.YHIGH=(\d+)", result)
    if not low or not high or int(high[1]) - int(low[1]) < 20:
        raise RenderError("HyperFrames snapshot has insufficient visual variation")


def _tool_signature():
    return {
        "renderer": json.loads((NODE / "hyperframes" / "package.json").read_text())["version"],
        "files": [
            PICTURE_CONTRACT_REVISION,
            *(
                _sha(file)
                for file in (
                    Path(__file__).with_name("scene.css"),
                    Path(__file__).with_name("scene_art.py"),
                    GSAP,
                    FONT,
                )
            ),
        ],
    }


def _shot_key(state, shot, ratio, frames, asset, tools):
    # Exclude timecode, planning-only references, audio, revision, and notes.
    value = {
        "tools": tools,
        "settings": [ratio, FPS, "looks", frames],
        "content": {
            "title": _hook_title(state, shot, state.get("selectedHook")),
            "brand": state["brief"].get("brand", ""),
            "product": state["brief"].get("product", ""),
            **{key: shot.get(key) for key in ("style", "motion", "beat", "caption", "trimMs")},
            "reveal": _reveal_ms(state, shot),
        },
        "asset": [asset[1]["role"], asset[1]["ext"], _sha(asset[0])] if asset else None,
    }
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _shot_render(state, shot, ratio, frames, asset_dir, cache, tools, cancelled):
    asset = _asset(state, shot.get("asset"), PICTURE_ROLES)
    source = (_asset_file(asset_dir, asset), asset) if asset else None
    key = _shot_key(state, shot, ratio, frames, source, tools)
    cached = cache / key
    video = cached / "picture.mp4"
    marker = cached / "verified.json"
    if cached.is_symlink() or marker.is_symlink():
        raise RenderError("Unexpected symlink in picture cache")
    if video.is_file() and marker.is_file():
        try:
            data = json.loads(marker.read_text())
            if not video.is_symlink() and data["sha256"] == _sha(video):
                return video, True
        except (OSError, ValueError, KeyError):
            pass
        raise RenderError("Invalid shot cache entry. Remove it and retry.")

    with tempfile.TemporaryDirectory(prefix="shot-", dir=cache) as directory:
        work = Path(directory)
        project = work / "composition"
        project.mkdir()
        _project(project, state, shot, ratio, frames, source)
        env = _hyperframes_env(work)
        command = ["node", HYPERFRAMES]
        _run([*command, "lint"], cwd=project, env=env, cancelled=cancelled, timeout=30)
        _run(
            [*command, "check", "--json", "--samples=3"],
            cwd=project,
            env=env,
            cancelled=cancelled,
            timeout=120,
        )
        snapshot_dir = work / "snapshots"
        samples = f"0,{frames / FPS / 2:.4f}"
        _run(
            [*command, "snapshot", "--at", samples, "--no-end", "--output", snapshot_dir],
            cwd=project,
            env=env,
            cancelled=cancelled,
            timeout=120,
        )
        snapshots = sorted(snapshot_dir.glob("frame-*.png"))
        if len(snapshots) != 2:
            raise RenderError("HyperFrames snapshot did not produce two frames")
        for file in snapshots:
            _check_snapshot(file, ratio, cancelled)
        result = work / "validated"
        result.mkdir()
        picture = result / "picture.mp4"
        _run(
            [
                *command,
                "render",
                "--quality",
                "looks",
                "--fps",
                str(FPS),
                "--workers",
                "1",
                "--frames-cache-dir",
                "off",
                "--output",
                picture,
            ],
            cwd=project,
            env=env,
            cancelled=cancelled,
            timeout=300,
        )
        _inspect_video(picture, ratio, frames, cancelled, decode=True)
        (result / "verified.json").write_text(json.dumps({"sha256": _sha(picture), "snapshots": 2}))
        for index, file in enumerate(snapshots):
            shutil.move(file, result / f"snapshot-{index}.png")
        _check_cancel(cancelled)
        try:
            result.rename(cached)
        except OSError:
            if cached.is_symlink() or marker.is_symlink() or not marker.is_file():
                raise
    return video, False


def _round_frames(milliseconds):
    return (milliseconds * FPS + 500) // 1000


def _timeline(state):
    """Assign frame counts from cumulative boundaries to avoid rounding drift."""
    cursor = 0
    result = []
    for shot in state["shots"]:
        end = cursor + shot["durationMs"]
        start_frame, end_frame = _round_frames(cursor), _round_frames(end)
        if end_frame <= start_frame:
            raise RenderError("A shot must contain at least one frame")
        result.append((shot, start_frame, end_frame - start_frame))
        cursor = end
    if not result:
        raise RenderError("Storyboard is empty")
    return result


def _audio_track_filters(tracks, asset_dir, state, duration_ms):
    """Keep audio inputs and filters independent of picture shot identities."""
    inputs, filters, labels, signatures = [], [], [], []
    for track in tracks:
        if track["atMs"] >= duration_ms or track["gain"] == 0:
            continue
        asset = _asset(state, track["asset"], AUDIO_ROLES)
        if not asset:
            raise RenderError("Audio track does not reference an audio asset")
        source = _asset_file(asset_dir, asset)
        index = len(signatures)
        signatures.append([track, _sha(source)])
        inputs.extend(["-protocol_whitelist", "file,pipe", "-i", source])
        trim = _seconds(track["trimMs"])
        duration = track["durationMs"]
        steps = [
            f"atrim=start={trim}:duration={_seconds(duration)}",
            "asetpts=PTS-STARTPTS",
            "aresample=48000",
            f"volume={float(track['gain']):.6f}",
        ]
        if track["fadeInMs"]:
            steps.append(f"afade=t=in:st=0:d={_seconds(track['fadeInMs'])}")
        if track["fadeOutMs"]:
            stop = _seconds(duration - track["fadeOutMs"])
            steps.append(f"afade=t=out:st={stop}:d={_seconds(track['fadeOutMs'])}")
        steps.append(f"adelay={int(track['atMs'])}:all=1")
        label = f"[track{index}]"
        filters.append(f"[{index}:a]" + ",".join(steps) + label)
        labels.append(label)
    return inputs, filters, labels, signatures


def _measure_loudnorm(file, cancelled):
    measurement = _ffmpeg(
        ["-i", file, "-af", AUDIO_LOUDNORM + ":print_format=json", "-f", "null", "-"],
        cancelled,
    )
    match = re.search(r'\{\s*"input_i"[^}]+\}', measurement)
    if not match:
        raise RenderError("Unable to measure audio loudness")
    levels = json.loads(match[0])
    if not math.isfinite(float(levels["input_i"])):
        raise RenderError("Audio tracks are silent or outside the timeline")
    return levels


def _mix_audio(state, asset_dir, cache, work, frames, cancelled):
    duration_ms = frames / FPS * 1000
    inputs, filters, labels, signatures = _audio_track_filters(state["tracks"], asset_dir, state, duration_ms)
    key_data = [AUDIO_MIX_VERSION, AUDIO_LOUDNORM, frames, signatures]
    key = hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
    output = cache / f"audio-{key}.wav"
    if output.is_file() and not output.is_symlink():
        return output, True, bool(labels)
    duration = _seconds(duration_ms)
    if labels:
        filters.append(
            "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=duration={duration}[mix]"
        )
        raw = work / "raw.wav"
        _ffmpeg(
            [
                "-v",
                "error",
                *inputs,
                "-filter_complex",
                ";".join(filters),
                "-map",
                "[mix]",
                "-ac",
                "2",
                "-ar",
                "48000",
                "-c:a",
                "pcm_f32le",
                "-y",
                raw,
            ],
            cancelled,
        )
        levels = _measure_loudnorm(raw, cancelled)
        if float(levels["output_i"]) < -14.75:
            # Reduce crest factor only when transients prevent reaching the loudness target.
            peak = 10 ** (float(levels["input_tp"]) / 20)
            threshold = min(0.5, max(0.000976, peak * 0.235))
            compressed = work / "compressed.wav"
            _ffmpeg(
                [
                    "-v",
                    "error",
                    "-i",
                    raw,
                    "-af",
                    f"acompressor=threshold={threshold:.6f}:ratio=4:attack=1:release=40:detection=peak",
                    "-c:a",
                    "pcm_f32le",
                    "-y",
                    compressed,
                ],
                cancelled,
            )
            raw = compressed
            levels = _measure_loudnorm(raw, cancelled)
        loudnorm = (
            AUDIO_LOUDNORM + ":"
            f"measured_I={levels['input_i']}:measured_TP={levels['input_tp']}:"
            f"measured_LRA={levels['input_lra']}:measured_thresh={levels['input_thresh']}:"
            f"offset={levels['target_offset']}:linear=true"
        )
        args = ["-i", raw, "-af", loudnorm]
    else:
        args = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    partial = work / "mixed.wav"
    _ffmpeg(
        ["-v", "error", *args, "-t", duration, "-ac", "2", "-ar", "48000", "-y", partial],
        cancelled,
    )
    _check_cancel(cancelled)
    os.replace(partial, output)
    return output, False, bool(labels)


def _audio_evidence(file, audible, cancelled):
    if not audible:
        return {"mode": "silent timeline"}
    result = _ffmpeg(
        ["-nostats", "-i", file, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
        cancelled,
    )
    summary = result.rsplit("Summary:", 1)[-1]
    level = re.search(r"I:\s*(-?[\d.]+) LUFS", summary)
    peak = re.search(r"Peak:\s*(-?[\d.]+) dBFS", summary)
    if not level or not peak:
        raise RenderError("Unable to verify export loudness and true peak")
    lufs, dbtp = float(level[1]), float(peak[1])
    return {
        "mode": "mixed tracks",
        "integratedLufs": lufs,
        "truePeakDbtp": dbtp,
        "targetLufs": -14,
        "maxTruePeakDbtp": -1.2,
        "targetMet": abs(lufs + 14) <= 1 and dbtp <= -1.2,
    }


def _decoded_frame(file, time_s, output, cancelled):
    _ffmpeg(
        ["-v", "error", "-ss", f"{time_s:.6f}", "-i", file, "-frames:v", "1", "-y", output],
        cancelled,
    )
    if not output.is_file():
        raise RenderError("Requested decode timestamp produced no frame")


def _picture_delta(snapshot, file, time_s, work, cancelled):
    frame = work / "compare.png"
    _decoded_frame(file, time_s, frame, cancelled)
    result = _ffmpeg(
        [
            "-i",
            snapshot,
            "-i",
            frame,
            "-filter_complex",
            "[0:v]scale=270:-2,format=yuv420p[a];[1:v]scale=270:-2,format=yuv420p[b];[a][b]ssim",
            "-f",
            "null",
            "-",
        ],
        cancelled,
    )
    similarity = re.search(r"All:([\d.]+)", result)
    if not similarity or float(similarity[1]) < 0.93:
        if os.environ.get("STUDIO_RENDER_DEBUG") == "1":
            print(result, flush=True)
        raise RenderError("Decoded export diverged from the reviewed HyperFrames snapshot")
    return float(similarity[1])


def _sheet(files, out, cancelled, *, columns=5):
    # Every frame is decoded before tiling. Pad the incomplete last row.
    filters = []
    args = []
    rows = math.ceil(len(files) / columns)
    for index, frame in enumerate(files):
        args.extend(["-i", frame])
        filters.append(
            f"[{index}:v]scale=220:300:force_original_aspect_ratio=decrease,"
            f"pad=220:300:(ow-iw)/2:(oh-ih)/2:color=0x171628[v{index}]"
        )
    positions = "|".join(
        f"{(index % columns) * 220}_{(index // columns) * 300}" for index in range(len(files))
    )
    if len(files) == 1:
        filter_graph = filters[0].replace("[v0]", "")
    else:
        join = "".join(f"[v{index}]" for index in range(len(files)))
        filters.append(f"{join}xstack=inputs={len(files)}:layout={positions}:fill=0x171628")
        filter_graph = ";".join(filters)
    _ffmpeg(
        [
            "-v",
            "error",
            "-filter_complex_threads",
            "1",
            *args,
            "-filter_complex",
            filter_graph,
            "-frames:v",
            "1",
            "-q:v",
            "2",
            "-y",
            out,
        ],
        cancelled,
    )
    return {"columns": min(columns, len(files)), "rows": rows}


def _render_ratio(state, timeline, ratio, asset_dir, cache, stage, tools, audio, cancelled):
    started = time.monotonic()
    folder = stage / f"work-{ratio}"
    folder.mkdir()
    rendered = []
    for shot, start, frames in timeline:
        file, hit = _shot_render(state, shot, ratio, frames, asset_dir, cache, tools, cancelled)
        rendered.append((file, hit, shot, start, frames))
    concat = folder / "shots.txt"
    entries = []
    for index, (picture, *_rest) in enumerate(rendered):
        name = f"shot-{index:03}.mp4"
        try:
            os.link(picture, folder / name)
        except OSError:
            shutil.copyfile(picture, folder / name)
        entries.append(f"file {name}")
    concat.write_text("\n".join(entries) + "\n")
    output = stage / f"master-{ratio}.mp4"
    frames = sum(shot[2] for shot in timeline)
    _ffmpeg(
        [
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "1",
            "-i",
            concat,
            "-i",
            audio,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-t",
            f"{frames / FPS:.6f}",
            "-movflags",
            "+faststart",
            "-y",
            output,
        ],
        cancelled,
    )
    meta = _inspect_video(output, ratio, frames, cancelled, audio=True, decode=True)
    comparison, grabs = [], []
    for index, (picture, _hit, shot, start, length) in enumerate(rendered):
        first = start / FPS
        mid = (start + length // 2) / FPS
        comparison.append(
            {
                "shot": shot["id"],
                "timeSeconds": round(first, 4),
                "snapshotToDecodedSsim": _picture_delta(
                    picture.parent / "snapshot-0.png", output, first, folder, cancelled
                ),
            }
        )
        still = folder / f"still-{index}.png"
        _decoded_frame(output, mid, still, cancelled)
        grabs.append(still)
    sheet = stage / f"contact-{ratio}.jpg"
    _sheet(grabs, sheet, cancelled)
    files = [output.name, sheet.name]
    if ratio == "9x16":
        thumbnail = stage / "thumbnail.jpg"
        _decoded_frame(output, 0, thumbnail, cancelled)
        files.append(thumbnail.name)
        # Nine frames around the payoff entrance, with 0.2-second spacing.
        payoff = next((start for shot, start, _ in timeline if shot["beat"] == "payoff"), 0)
        strip = []
        for i in range(min(9, math.ceil(frames / 6))):
            moment = max(0, min(payoff - 12, frames - 49)) + i * 6
            still = folder / f"strip-{i}.png"
            _decoded_frame(output, moment / FPS, still, cancelled)
            strip.append(still)
        action_sheet = stage / "action-strip.jpg"
        _sheet(strip, action_sheet, cancelled, columns=5)
        files.append(action_sheet.name)
    shutil.rmtree(folder)
    return files, {
        **meta,
        "pictureCacheHits": sum(item[1] for item in rendered),
        "pictureRendered": sum(not item[1] for item in rendered),
        "seconds": round(time.monotonic() - started, 3),
        "previewAgreement": comparison,
    }


def _render(state, asset_dir, out, cache, ratios, cancelled, *, hook_preview=False):
    _check_cancel(cancelled)
    _installed()
    started = time.monotonic()
    asset_dir, out, cache = map(lambda p: Path(p).absolute(), (asset_dir, out, cache))
    if out.is_symlink() or (out.exists() and (not out.is_dir() or any(out.iterdir()))):
        raise RenderError("Render destination must be a new or empty directory")
    if cache.is_symlink():
        raise RenderError("Render cache cannot be a symlink")
    out.parent.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    timeline = _timeline(state)
    frames = sum(item[2] for item in timeline)
    tools = _tool_signature()
    with tempfile.TemporaryDirectory(prefix=".render-", dir=out.parent) as directory:
        work = Path(directory)
        stage = work / "delivery"
        stage.mkdir()
        audio, reused_audio, audible = _mix_audio(state, asset_dir, cache, work, frames, cancelled)
        formats = {}
        names = []
        # Each cut is independent. Bounded parallelism keeps Chromium process count predictable.
        stopped = Event()

        def interrupted():
            return stopped.is_set() or cancelled()

        with ThreadPoolExecutor(max_workers=min(3, len(ratios))) as pool:
            jobs = {
                pool.submit(
                    _render_ratio, state, timeline, ratio, asset_dir, cache, stage, tools, audio, interrupted
                ): ratio
                for ratio in ratios
            }
            try:
                finished = {jobs[job]: job.result() for job in as_completed(jobs)}
            except BaseException:
                stopped.set()
                raise
        for ratio in ratios:
            files, stats = finished[ratio]
            formats[ratio] = stats
            names.extend(files)
        loudness = _audio_evidence(stage / "master-9x16.mp4", audible, cancelled)
        stats = {
            "renderer": f"HyperFrames {tools['renderer']}",
            "pictureCacheHits": sum(item["pictureCacheHits"] for item in formats.values()),
            "pictureRendered": sum(item["pictureRendered"] for item in formats.values()),
            "audioCacheHit": reused_audio,
            "seconds": round(time.monotonic() - started, 3),
            "formats": formats,
            "audio": loudness,
            "snapshotChecks": "PNG bounds, luma range, decoded start-frame SSIM",
            "hookPreview": bool(hook_preview),
        }
        (stage / "media-evidence.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
        (stage / "captions.srt").write_text(srt_captions(state), encoding="utf-8")
        names.extend(["media-evidence.json", "captions.srt"])
        if hook_preview:
            renamed = []
            for name in names:
                new_name = f"hook-{hook_preview}-{name}"
                (stage / name).rename(stage / new_name)
                renamed.append(new_name)
            names = renamed
        _check_cancel(cancelled)
        if out.is_dir():
            out.rmdir()
        stage.rename(out)
    return {"files": names, "stats": stats, "verified": loudness.get("targetMet", True)}


def render_campaign(state, asset_dir, out, cache, cancelled=lambda: False):
    """Render picture, audio, and final assembly as separate dependencies."""
    return _render(state, asset_dir, out, cache, tuple(FORMAT_SIZES), cancelled)


def render_hook(state, asset_dir, out, cache, hook_id, cancelled=lambda: False):
    """Render the opening three seconds with the requested single-variable hook."""
    if hook_id not in {hook["id"] for hook in state["hooks"]}:
        raise PreviewError("Unknown hook")
    remaining = 3000
    shots = []
    for shot in state["shots"]:
        if remaining <= 0:
            break
        duration = min(remaining, shot["durationMs"])
        shots.append({**shot, "durationMs": duration})
        remaining -= duration
    return _render(
        {**state, "shots": shots, "selectedHook": hook_id, "tracks": []},
        asset_dir,
        out,
        cache,
        ("9x16",),
        cancelled,
        hook_preview=hook_id,
    )
