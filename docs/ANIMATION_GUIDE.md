# Animation Guide — HyperFrames vs Remotion vs Code-Rendered vs Realistic Models

> v2, rewritten 5 Nov 2026 from full local reads of the repos, with live renders
> proven on this machine. Star counts are live-checked 5 Nov 2026 unless marked
> snapshot. Re-verify before you trust a number — stars change daily.

## The honest stack

- **Motion graphics / templated ads: HyperFrames or Remotion.** Both are proven
  on this machine (HyperFrames rendered a real 8s 9:16 Diwali ad; Remotion
  rendered a 2s 720p test). No GPU needed for basic motion, but local Linux
  render is the slow path — budget about 7s of render per 1s of 1080x1920 video.
- **Realistic footage: client-supplied clips or licensed stock (Pexels, Pixabay,
  Coverr), composited in HyperFrames/Remotion — or, optionally, one shot from a
  paid cloud video API (Kling, Veo, Runway, Luma). No local GPU model in this
  repo; nothing here needs a GPU.
- **Prototyping / assembly: MoneyPrinterTurbo.** Fenced off — never the paid hero
  ad, never its bundled music.
- No single tool here is a one-stop ad machine on its own.

## The four paths

### 1. Code-rendered — HyperFrames (TypeScript / Node 22+, 79,214 stars, Apache-2.0)

- What: write HTML, render MP4. A video is an `index.html` root composition
  that mounts one scene per sub-composition file from `compositions/`.
  Animations are seekable — a paused GSAP timeline registered on
  `window.__timelines["<composition-id>"]`. The renderer seeks the paused
  timeline frame by frame in headless Chrome and encodes with FFmpeg, so the
  same input produces the same video (deterministic).
- When: you need motion graphics, kinetic type, many versions of one template,
  or a repeatable ad. This is the primary renderer for this repo.
- Needs: Node.js 22+, FFmpeg. No GPU for basic motion (software-GPU slow path
  on local Linux). Run `npx hyperframes browser ensure` once (Chrome Headless
  Shell, about 3 min first time).
- Install: `npx hyperframes` / `npx skills add heygen-com/hyperframes`.
  There is NO pip package for HyperFrames — it is installed with npx, not pip.
  Read the `/hyperframes` skill first, then `/hyperframes-cli`,
  `/hyperframes-registry`, `/media-use`. Search the registry (~450 blocks and
  components) with `catalog` before hand-building any named visual.
- Licence: Apache-2.0, no per-render fees, no commercial-use threshold.
- Good for: kinetic type, product launch templates, Diwali price versions,
  UGC templates, batch versions via root variables + `render --batch rows.json`.
- Render loop: `npx hyperframes lint` → `npx hyperframes check --json` →
  `npx hyperframes snapshot` (look at the PNG frames) → `npx hyperframes render`.
  Passing checks alone is not a reason to render; look at frames first.
- Environment traps (proven): render needs at least 1 GB free at `os.tmpdir()`
  AND the output dir — /tmp on this machine is a 512 MB tmpfs, so render under
  the workspace with `TMPDIR=<workspace>/tmp`. For the legacy example and
  scaffolds, `npm ci` installs GSAP and prepares `assets/gsap.min.js`.
  Render with the local asset.
- Full contract: `skills/ad-animation-motion/references/render-contract.md`.
  Proven example: `examples/hyperframes-diwali-8s/` (8s, 1080x1920, rendered here).

### 2. Code-rendered — Remotion (Node 20+, React, 70,893 stars, source-available)

- What: video in React. You write code, it renders video. Templates, versions,
  data-driven. "React code is the source of truth."
- When: you need many versions (price, city, language), a template, or a
  repeatable ad, and your team works in React.
- Needs: Node `^20.19.0 || ^22.13.0 || >=24` for new scaffolded projects
  (library floor is Node 16). FFmpeg and Chrome are auto-downloaded by Remotion.
  No GPU for basic motion; GPU helps blur, 3D, and video decoding only.
- Install: `npx create-video@latest` (or `--yes --blank my-video`). All
  `@remotion/*` packages must be pinned to the same exact version.
- Licence: **source-available, NOT open source** (proprietary Remotion Licence).
  Free for up to 3 people — an individual, a for-profit organisation with up
  to 3 employees, a non-profit, or non-commercial evaluation. A Company Licence
  is needed at **4+ people total headcount** (headcount, NOT revenue — the
  licence contains no revenue test at all). Pricing: Creators $25/month per person
  who writes Remotion code; Automators $0.01 per render, $100/month minimum.
  A licence change is announced for Remotion 5.0 (mandatory telemetry for
  Automators). 9:16 is `width={1080} height={1920}`; the TikTok template
  already ships that as a captioned-video template. Captions are first-class
  (`@remotion/captions`, SRT/VTT, Whisper). Versioning is JSON `inputProps` +
  the `dataset-render` batch pattern. Lambda renders a 15s ad for about
  $0.001–0.01 warm. Do not let users upload their own Remotion code to your
  service for rendering — your service must generate the code (or an LLM must).
- Good for: kinetic type, product launch templates, Diwali price versions,
  UGC templates.
- Proven here: a blank 2s 720p render completed in about 85s including bundling
  (blank content — the pipeline is proven, not the content).

### 3. Code-rendered film styles — lemo-opuscar + mg-styles-15 (the style library)

- lemo-opuscar (lemomo-ai/lemo-opuscar, 12,443 stars, MIT code / CC BY 4.0 demo
  films): 66 film styles in code, each a STYLE.md in the same 11 sections
  (essence + what it is not, materials, colour logic, type, motion, camera
  grammar, sound, native moves, pitfalls, engine, variation). Needs Node 20+,
  ffmpeg 7+ (6.x breaks loudnorm), Python 3.11+. Films are 30–60s, 1920x1080,
  24 fps by default. Render contract: `window.render(t)` pure function of t,
  `window.READY`, `window.DUR`, `window.EV`, `window.TEXTS`. Audio is half the
  film: TTS + ASR check, score from the cue map, mix to -14 LUFS. Fonts must be
  downloaded before rendering — the demo ships licence texts, not font files.
  Proven here: a 3s 9:16 film rendered at exactly 3.000s, muxed to -14.0 LUFS.
- mg-styles-15 (Vincentwei1021/mg-styles-15, MIT): 15 ten-second motion-design
  films, each with its full prompt (~95 lines) and complete source. Prompt
  template: role + benchmarks, fixed output spec (1920x1080, 30 fps, exactly
  10.000s, -14 LUFS), tech route, creative seed (second-by-second beats),
  signature features with checkable numbers, how-to-work, rules (determinism,
  licences), craft checklist + self-score, deliver + report. Needs Node 22.12+,
  Chrome, ffmpeg, Python 3.11+. Proven here: full 10s video rendered, audio
  measured -13.70 LUFS at exactly 10.000s.
- Our styles in `prompts/mg-styles.md` follow the lemo 11-section format and
  the mg prompt template. They are original — inspired by the patterns, not copied.

### 4. Realistic footage — supplied / licensed stock + optional paid cloud API

- What: realistic footage for an ad comes from three routes, in this order:
  (1) client-supplied clips — the supplied clip is the truth, never regenerate
  the product; (2) licensed stock — Pexels, Pixabay, Coverr, searched with the
  shot brief's keywords, licence checked per clip; (3) optionally, one shot
  from a paid cloud video API (Kling, Veo, Runway, Luma) when no stock or
  supplied clip can cover the shot.
- When: you need a realistic scene and cannot shoot it. A street, a home, a
  festival. Stock is for atmosphere and B-roll; the product moment uses
  supplied footage or a real shoot.
- Needs: nothing beyond the core stack. Stock and supplied clips composite in
  HyperFrames/Remotion on CPU. Cloud APIs render in the cloud and are paid,
  third-party services — no install here, no verified install instructions in
  this repo; check each service's pricing, terms, and commercial-use rights
  yourself before spending.
- Limits: stock is generic — it cannot show your exact product, store, or
  offer. A generated cloud clip is not proof the product looks right; hands,
  faces, and text are known failure modes, and character consistency across
  clips is not guaranteed. Check every clip frame by frame. Never use a real
  person without written consent.
- Rules: one brief per shot (subject, action, camera, light, style, negative);
  3 candidates or takes per shot, pick the best; lock character, wardrobe, and
  light across shots; grade after the cut is locked.
- **No local GPU video model is part of this repo.** The whole core stack runs
  without a GPU. Do not recommend installing or running one.

### 5. Short-video assembly — MoneyPrinterTurbo (139,492 stars, MIT code)

- What: a faceless-shorts factory. Topic in, narrated stock/AI montage short out.
  Script (LLM) → voice (TTS) → footage search → subtitles → music → render.
- **Fenced off: prototyping and assembly only. NEVER the paid hero ad.**
  No product accuracy (generic keyword-matched stock), no brand kit, no CTA,
  no exact-duration control, free voice is recognisably synthetic.
- **NEVER its bundled music in a paid ad** — the bundled songs are
  YouTube-sourced and the README flags the copyright risk.
- Free path ($0): Ollama (script) + Edge TTS (voice) + Pexels/Pixabay/Coverr
  (free registration keys) + local render. Legitimate roles: hook/script/
  voiceover prototyping before a real shoot; render/assembly when all media is
  human-supplied; bulk organic cutdowns around a campaign.
- Security: keys live in plaintext `config.toml`, API auth is off by default,
  default listen host is 0.0.0.0 — harden to 127.0.0.1 with an `api_key`,
  never commit or share `config.toml` or a settings export.

## When to use which

| Need | Use |
|---|---|
| Many versions, same template | HyperFrames or Remotion |
| Kinetic type, motion graphics | HyperFrames or Remotion, style from `prompts/mg-styles.md` |
| Realistic scene, no shoot | Supplied/licensed stock in HyperFrames/Remotion, or one paid cloud API shot |
| Image-to-video, style, upscale | Not in this repo's CPU stack — supplied footage or a paid cloud API |
| One-off hero moment | Keyframes, not a template |
| Fast hook test (3 seconds) | HyperFrames — fastest to iterate here |
| Rough-cut prototyping only | MoneyPrinterTurbo, fenced off, never the hero ad |

## Hardware needs

- Code-rendered: laptop is fine. Node 20+ / 22+ + ffmpeg 7+. No GPU for basic
  motion, but local Linux render is the slow path (about 7s per 1s of 1080x1920).
- Realistic footage: no GPU needed. Stock and supplied clips composite on CPU;
  cloud APIs render in the cloud (paid).
- **/tmp trap:** /tmp on this machine is a 512 MB tmpfs. Render under the
  workspace and set `TMPDIR` there, or renders fail with no disk space.

## Requirements — baseline

```bash
ffmpeg -version   # 7+
node --version    # 20+ (22+ for HyperFrames, 22.12+ for mg-styles-15)
python3 --version # 3.11+
npx hyperframes --version  # 0.9.15 proven here
```

## ffmpeg — the workhorse

- Cut, trim, captions, resize, reframe 9:16 / 1:1 / 16:9, loudness.
- Example: `ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:a copy out-9x16.mp4`
- Always check the output on a phone, not only on desktop.

## Render pipeline (recommended)

1. Treatment first — before opening any demo or example. 3 structures, logline,
   shot list, beat sheet, cue map, sound table.
2. Hook test: 3 seconds, HyperFrames, on a phone, sound-off.
3. Full motion pass: HyperFrames or Remotion for type and templates.
4. Realistic footage: supplied or licensed stock clips, 3 candidates per shot,
   pick the best; or one paid cloud API shot. Check every clip frame by frame.
5. Review loop: contact sheets, 0.2s strips, full-speed watch, one fix round,
   then a second-AI jury scored on a rubric.
6. Edit: cut, captions, sound -14 LUFS (measured, not assumed), export
   9:16 + 1:1 + 16:9.
7. QA: claims, consent, licences, platform rules. Sign-off.

## What not to do

- Do not render the full ad before the 3-second hook test passes.
- Do not use a realistic model for a 30-second single shot. It will drift.
  Cut into about 5s shots and stitch.
- Do not use face-swap / Deep-Live-Cam on real people. This repo has no face-swap workflow.
- Do not assume a model licence allows commercial use. Check it.
- Do not render in /tmp on a machine with a small tmpfs. Render under the workspace.
- Do not trust a finished render as factual validation — claims, prices, and
  product details need separate checks.
