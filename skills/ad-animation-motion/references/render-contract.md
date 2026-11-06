# Render contract — reference for ad-animation-motion

Read this before writing any code-rendered ad. This is the contract the
HyperFrames renderer actually enforces, proven by a real render on this machine.

## HyperFrames basics
HyperFrames is TypeScript / Node 22+. There is no pip package. Install with
`npx hyperframes` or `npx skills add heygen-com/hyperframes`. Licence: Apache-2.0,
no per-render fees, no commercial-use threshold. Read the /hyperframes skill
first, then /hyperframes-cli, /hyperframes-registry, /media-use.
Search the registry (~450 blocks and components) with `catalog` before
hand-building any named visual. Install with `hyperframes add <name>`.

## Project shape
`index.html` (root composition, data-composition-id, data-duration, data-width,
data-height) + `compositions/*.html` (one file per scene, everything inside
`<template>`, root styled as `#root` with `inset: 0`). Timed elements live in
sub-compositions — never nest timed elements in the root, lint warns on it.

## Clip rules
- Every timed element: `class="clip"`, `data-start` + `data-duration` (seconds).
  Video length is the root's `data-duration`; overrun is cut.
- One paused timeline per composition, registered as
  `window.__timelines["<composition-id>"] = gsap.timeline({ paused: true })`.
- Use `fromTo`, never `from` — a `from` records its start state once and drifts
  on seek-back. Never `add()` a scene timeline to the root's; the runtime
  drives each scene itself.
- Never tween `display`, `visibility`, or `autoAlpha` on a `.clip` — animate a child.
- No CSS `transform` on an element GSAP transforms; animate transforms, not
  left/top/width/height. Host id must equal scene id, or a scene stalls.

## Determinism
Everything visible is a pure function of timeline time. No `Date.now()`,
no unseeded `Math.random()`, no network fetches, no timers, no `repeat: -1`.
Seeded randomness only (a mulberry-style seeded RNG). Any frame must be
renderable alone, in any order, by any worker.

## Fonts first
Only the bundled families resolve by name. Anything else needs `@font-face`
to a file in `assets/fonts/`. Download OFL fonts BEFORE rendering and verify
`document.fonts.load` resolves. A missing font kills the render with a bare
network error and a misleading timeout — check fonts first.

## The loop
`npx hyperframes lint` (static) -> `npx hyperframes check --json` (browser gate:
lint, runtime, layout, motion, contrast) -> `npx hyperframes snapshot` (look at
the PNG frames) -> `npx hyperframes render`. Passing checks alone is not a
reason to render; look at frames first.

## Vertical numbers (1080x1920)
Top 168px clear. All words and product inside 168-1330px. Below 1330px only
texture and decoration. Minimum 28px type. About 5 words per claim line.
Frame 0 is the thumbnail: face, result, or one bold line already on screen.
Never black, never a logo.

## Motion values (measured)
Arrivals `expo.out` / `power4.out`. Exits 40-50% shorter than entrances.
Next element starts at 30-50% of the previous one. Stagger letters 1 frame,
words 60-120ms, items 40-80ms. Holds 0.5s + 0.3s per word; last line at least
2s. Titles 4-9% of frame height. Beat grid: fps x 60 / BPM.

## Audio discipline
Cue map first; picture locks to the music grid. Voice: TTS per line, ASR-checked,
word timings kept. Foley from event times. Mix to -14 LUFS, true peak -1.2 dB.
Subtitle hold at least max(1.8s, speech + 0.6s). Text hold about letters/15 + 1.5s.

## Environment traps (proven)
- Render needs at least 1 GB free at `os.tmpdir()` AND the output dir. /tmp on
  this machine is a 512 MB tmpfs — render under the workspace with
  `TMPDIR=<workspace>/tmp` and `--frames-cache-dir` under the workspace.
- In the legacy GSAP example and scaffold, `npm ci` prepares the local
  `assets/gsap.min.js` dependency from the pinned package.
  Preserve its notices and use the local asset at render time.
- Run `npx hyperframes browser ensure` once (Chrome Headless Shell, ~3 min
  first time). `check`, `snapshot`, and `render` need headless Chrome; `lint`
  does not. Local Linux render is the slow path: about 7s of render per 1s of
  1080x1920 video. Use `draft` to iterate, `looks`, then `delivery` for final.
- Batch versions with root variables + `render --batch rows.json`.

## Treatment first, and the jury
Write the treatment BEFORE opening any demo or example: 3 candidate structures,
logline, shot list, second-by-second beat sheet, cue map, sound table.
Never rebuild a demo's story, arc, shots, props, or timeline.
The "not the demo again" check: at least 4 of 6 must differ from the demo —
structure, opening, signature shot, camera path, score shape, ending.
Review loop: contact sheets, 0.2s strips, full-speed watch, ONE fix round.
Then a second-AI jury scores the film on a rubric (aim 9/10, fix the lowest
score first) with an honest top-3 weaknesses list.
