---
name: ad-animation-motion
description: >-
  Animate motion graphics, kinetic type, and transitions for social ads, and render them with the HyperFrames or Remotion code-rendered path. Use when an ad needs motion, kinetic type, a renderable template, or many versions from one template, or when text must move with the joke. Trigger phrases: 'animate this', 'kinetic type', 'render the ad', 'make a template', 'motion test'. Delivers a motion map and a rendered pass. Do NOT use for realistic AI video — that is the realistic-video skill — and never invent a render path; follow the render contract in references/render-contract.md.
license: MIT
---
# Ad Animation / Motion

## When to use
- The ad is motion graphics, kinetic type, or a template that must render many versions.
- Text needs to move with the joke, not sit still.
- You need a repeatable render: same ad, new price, new city, new language.

## Workflow
1. Read the script and the motion styles in `prompts/mg-styles.md`. Pick ONE style.
   One style per ad. Do not mix five styles.
2. Set the timing grid: 24 or 30 fps, 9:16, 1080x1920. Hook frame at 0.0–1.5s.
   Text in by 0.3s, out by 1.2s. No text that lingers for 5 seconds.
   Vertical numbers: top 168px clear, text band 168–1330px, min 28px type,
   about 5 words per line, frame 0 is the thumbnail. Exits 40–50% shorter
   than entrances, next element starts at 30–50% of the previous one,
   holds 0.5s + 0.3s per word.
3. Animate in this order: hook text, product, payoff text, CTA. Each element enters once,
   clearly, with ease-out. No element should bounce, spin and slide at the same time.
4. Use the code-rendered path when you need versions: Remotion (Node 20+, React) or HyperFrames (TypeScript / Node 22+, HTML). HyperFrames is NOT Python — there is no pip package.
   See `docs/ANIMATION_GUIDE.md` for when to use which, and `references/render-contract.md` for the exact render contract. Both render from code, so a price
   change is a data change, not a re-edit.
5. Use keyframes when you need a one-off hero moment, not a template.
   Treatment first: write the treatment before opening any demo or example, and
   run the 'not the demo again' check — at least 4 of 6 must differ from the demo
   (structure, opening, signature shot, camera path, score shape, ending).
6. Fonts first: download OFL fonts before rendering and verify they load — a missing
   font kills the render with a bare network error. Vendor GSAP locally
   (`assets/gsap.min.js`); never rely on a CDN at render time.
7. Render loop: `lint` → `check --json` → `snapshot` (look at the frames) → `render`.
   Passing checks alone is not a reason to render. Export a motion test first:
   3 seconds, hook only. Watch it on a phone, sound-off. If the hook text is
   not readable in 1 second, fix timing before rendering the full ad.
8. Determinism: every frame is a pure function of timeline time. Seeded
   randomness only. No `Date.now()`, no unseeded `Math.random()`, no network
   fetches, no timers, no `repeat: -1`. Use `fromTo`, never `from`.
7. Hand off to the editor with the render files, frame rate, and export settings.

## Output format
- Style: name from mg-styles.md + why this ad
- Timing grid: fps, duration, hook in/out times
- Motion map: element, enter, hold, exit — per beat
- Render path: Remotion / HyperFrames / keyframes + commands
- Motion test: 3-second hook test, pass / fail notes

## Quality bar
- Text is readable at 1 second, on a phone, sound-off.
- Motion has one idea per beat. No decoration for its own sake.
- The CTA text is the biggest, clearest text in the ad.
- A version change (price, city, language) takes minutes, not a re-edit.

## Examples
- Kinetic type: hook words appear one by one, on the beat, then the product lands.
- Pop / sticker: elements pop in with a small overshoot, then settle. Good for Gen-Z.
- Smooth premium: slow ease, gold shimmer, no bounce. Good for jewellery.
- See `prompts/mg-styles.md` for 15 original styles with duration, fps, palette, motion rules.

## Anti-patterns
- Text that flies in from three directions at once.
- A transition every second. Pick one transition style.
- Motion that is faster than the viewer can read.
- Rendering the full ad before testing the 3-second hook.

## Render contract
- Read `references/render-contract.md` before writing any composition.
- HyperFrames: one paused timeline per composition on `window.__timelines`,
  `class="clip"` + `data-start`/`data-duration`, `fromTo` not `from`.
- Render under the workspace with `TMPDIR` set there — /tmp is a 512 MB tmpfs.
- Review loop: contact sheets, 0.2s strips, full-speed watch, one fix round,
  then a second-AI jury scored on a rubric (aim 9/10, fix the lowest first).

## References
- `references/render-contract.md` — Render contract — HyperFrames clip rules, timelines, the lint-check-snapshot-render loop, vertical numbers, motion values.
- Read only the reference file for the step you are on; do not load every reference at once.
