#!/usr/bin/env python3
"""Build the original Quiet Hours art, local clip, and sound without cloud calls."""

import argparse
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from studio.scene_art import KEYS, MAT  # noqa: E402


def svg(content):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="760" height="560" viewBox="0 0 760 560">
<defs><pattern id="weave" width="13" height="13" patternUnits="userSpaceOnUse">
  <path d="M-2 2l4-4m-4 17L15-2M11 15l4-4" stroke="#a5b8ff" stroke-width="2" opacity=".48"/>
</pattern></defs>{content}</svg>"""


PACKSHOT = svg(
    MAT
    + """
<g transform="rotate(-10 395 145)">
  <path d="M124 141l40-31 40 31-40 31z" fill="#c0ef3f" stroke="#171628" stroke-width="5"/>
  <path d="M152 140l9 8 15-17" fill="none" stroke="#171628" stroke-width="5"/>
</g>"""
)
PLANNING = svg(
    """<rect width="760" height="560" fill="#ee00bb"/>
<path d="M45 47H715V513H45zM380 47v466M45 280h670" fill="none" stroke="#251329" stroke-width="4" stroke-dasharray="10 10"/>
<rect x="100" y="194" width="560" height="172" fill="#251329"/>
<text x="380" y="276" text-anchor="middle" font-family="Arial,sans-serif" font-size="46" font-weight="bold" fill="#fff">FRAMING SKETCH</text>
<text x="380" y="319" text-anchor="middle" font-family="Arial,sans-serif" font-size="23" fill="#fff">KEYS • OVERHEAD • ROUGH</text>"""
)
CLIP_BACKDROP = svg(
    """<rect width="760" height="560" fill="#e5deff"/>
<path d="M26 40h70m-35-35v70m602 448h70m-35-35v70" stroke="#263eb5" stroke-width="3"/>
<path d="M40 115h680m-680 340h680" stroke="#263eb5" stroke-opacity=".25" stroke-width="2" stroke-dasharray="5 9"/>"""
    + MAT
)
KEYS_IMAGE = svg(KEYS)


def make_score(destination):
    sample_rate = 48000
    noise = random.Random(781)
    events = [(0.08, 148, 0.24), (0.19, 603, 0.13), (2.49, 304, 0.13)]
    events.extend((i * 0.52, 126 if i % 2 else 184, 0.17) for i in range(1, 28) if i not in {17, 18, 19})
    events.extend([(8.24, 312, 0.23), (10.25, 82, 0.30), (12.08, 248, 0.20), (12.15, 372, 0.16)])
    samples = [0.0] * (15 * sample_rate)
    for start, frequency, amplitude in events:
        offset = round(start * sample_rate)
        for index in range(min(sample_rate // 3, len(samples) - offset)):
            t = index / sample_rate
            envelope = min(1, t * 450) * math.exp(-18 * t)
            tone = math.sin(2 * math.pi * frequency * t) * 0.8
            click = noise.uniform(-1, 1) * math.exp(-67 * t) * 0.2
            samples[offset + index] += amplitude * envelope * (tone + click)
    with wave.open(str(destination), "wb") as file:
        file.setparams((1, 2, sample_rate, 0, "NONE", "not compressed"))
        file.writeframes(b"".join(struct.pack("<h", round(sample * 32767)) for sample in samples))


def make_assets(output):
    output = Path(output).absolute()
    output.mkdir(parents=True, exist_ok=True)
    names = ("packshot.png", "planning-reference.png", "key-drop.mp4", "desk-score.wav")
    if any((output / name).exists() for name in names):
        raise FileExistsError("Use a new directory for the original demo assets")
    with tempfile.TemporaryDirectory(prefix=".quiet-hours-", dir=output) as directory:
        work = Path(directory)
        manifest = work / "illustrations.json"
        manifest.write_text(
            json.dumps(
                {
                    "packshot.png": PACKSHOT,
                    "planning-reference.png": PLANNING,
                    "clip-backdrop.png": CLIP_BACKDROP,
                    "keys.png": KEYS_IMAGE,
                }
            )
        )
        subprocess.run(["node", HERE / "make_art.mjs", work, manifest], check=True, timeout=60)
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-loop",
                "1",
                "-framerate",
                "30",
                "-i",
                work / "clip-backdrop.png",
                "-loop",
                "1",
                "-framerate",
                "30",
                "-i",
                work / "keys.png",
                "-filter_complex",
                "[1:v]scale=530:390[keys];"
                "[0:v][keys]overlay=x=110:y='if(lt(t,1),-300+420*t,120-14*sin((t-1)*9)*exp(-(t-1)*5))'",
                "-t",
                "4",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-threads",
                "2",
                "-movflags",
                "+faststart",
                work / "key-drop.mp4",
            ],
            check=True,
            timeout=60,
        )
        make_score(work / "desk-score.wav")
        for name in names:
            shutil.move(work / name, output / name)
    return [output / name for name in names]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    for asset in make_assets(parser.parse_args().output):
        print(asset)
