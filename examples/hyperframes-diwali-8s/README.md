# HyperFrames Diwali Ad — 8s, 9:16, Proven Render

A complete, working HyperFrames project: an 8-second vertical Diwali ad for
"Test Jewellers" — gold bangles, flat 20% off making charges. Three beats:

- 0–2.5s hook: "✦ DIWALI ✦ / Gold that glows / like the festival itself"
- 2.5–5.5s product: "Gold Bangles / Flat 20% OFF making charges"
- 5.5–8s CTA: "Test Jewellers / Shop Now / This Diwali, wear the light"

## Proof

This project rendered end-to-end on this machine (Node v24, ffmpeg 8.1,
HyperFrames CLI 0.9.15, no GPU) on 5 Nov 2026: **8.000s, 1080x1920, 30 fps,
H.264, 523,945 bytes, 240/240 frames**, verified with ffprobe and by decoding
frames at t=0/1/3/5/7s. The render took about 58s (local Linux screenshot +
software-GPU slow path — about 7s of render per 1s of video).

## What is inside

- `index.html` — root composition (`data-composition-id="main"`,
  `data-duration="8"`, 1080x1920) hosting three sub-compositions.
- `compositions/hook.html`, `product.html`, `cta.html` — one scene each,
  everything inside `<template>`, one paused GSAP timeline per composition
  registered on `window.__timelines`, `fromTo` only (never `from`).
- `hyperframes.json`, `package.json`, `package-lock.json`, `meta.json`.
  The lock pins HyperFrames 0.9.15 and GSAP 3.15.0. The npm setup generates
  `assets/gsap.min.js` locally with the upstream notices intact.
- The saved `rendered-test.mp4` and HyperFrames captures are local evidence.
  This example reproduces them from source.

## How to render it (from this folder)

```bash
npm ci
mkdir -p "$PWD/tmp"
export TMPDIR="$PWD/tmp"
npm run lint
npm run check -- --json
npm run snapshot -- --at 0,1,3,4,6,7.5   # inspect the frames first
npm run render -- --quality looks -o rendered-test.mp4
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  -of default=noprint_wrappers=1 rendered-test.mp4
```

Notes:

- The render requires at least 1 GB free in both `TMPDIR` and the output directory.
- GSAP is installed from npm. Retain its notices and review the
  [GSAP Standard License](https://gsap.com/standard-license/) for your use.
  The legacy examples run authored timelines in a browser. Super Ads Studio
  uses its own scene animation code.
- Run `npx hyperframes browser ensure` once first (Chrome Headless Shell,
  about 3 min the first time). `check`, `snapshot`, and `render` need
  headless Chrome; `lint` does not.
- Vertical numbers used here: top 168px clear, text band 168–1330px, min
  28px type, about 5 words per line, frame 0 shows the hook (never black,
  never a logo). Text holds are 0.5s + 0.3s per word; the last line holds
  at least 2s.
- To make your own version: copy this folder, change the words and the
  colours, keep the structure — or run
  `python3 ../../scripts/new_ad.py --brand X --product Y --format reel15 --hyperframes`.
  Treatment first, and run the "not the demo again" check: at least 4 of 6
  must differ from this demo (structure, opening, signature shot, camera
  path, score shape, ending).
