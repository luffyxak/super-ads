---
name: ad-realistic-video
description: >-
  Work with realistic footage for ads — client-supplied clips or licensed stock (Pexels, Pixabay, Coverr), composited in HyperFrames or Remotion, or optionally one shot from a paid cloud video API (Kling, Veo, Runway, Luma). Use when you need a real-looking scene and cannot shoot it, when the client has footage, or when a realistic shot is worth paying a cloud service for. Trigger phrases: 'realistic footage', 'stock footage', 'use the client's video', 'cloud video API'. Do NOT use a local GPU video model — this repo has none — and never generate a real person without written consent.
license: MIT
---

# Ad Realistic Video

## When to use
- You need a realistic scene and cannot shoot it: a street, a home, a festival, a product in use.
- The client has supplied footage, or licensed stock fits the shot.
- One realistic shot is worth paying a cloud video API for (Kling, Veo,
  Runway, Luma — paid third-party services, no local GPU needed).
- You need many variations of the same scene for testing.

This repo has NO local GPU video model. The whole core stack runs without a
GPU: HyperFrames (primary, proven here) + Remotion + code-rendered patterns.
Do not recommend installing or running a local video model. Do not use this
for a same-day rush without a fallback.

## Workflow
1. Start from the shot list. One shot brief per shot. Write it in this order:
   subject, action, camera, light, style, negative. Shot briefs live in
   `prompts/video-prompts.md` (realistic-footage section). Keep briefs original.
2. Route each shot: (a) client-supplied footage — use it as shot, it is the
   truth, never regenerate the product; (b) licensed stock — search Pexels,
   Pixabay, or Coverr with the shot brief's keywords, check the licence per
   clip; (c) paid cloud video API — only for a shot no stock or supplied
   clip can cover, one shot at a time, paid, third-party terms apply.
3. Lock consistency: same character description, same wardrobe, same light
   across shots. Write the character description once and paste it into every
   brief. If the face changes, the ad breaks.
4. Get 3 takes or 3 candidate clips per shot. Pick the best. Do not use the
   first one by default.
5. Check realism frame by frame: hands, teeth, text in frame, logos, physics.
   Stock and cloud clips can both carry wrong text, wrong logos, and wrong
   products. Fix or cut. The product must look like the real product: colour,
   shape, label, size.
6. Never generate or use a real person's face, voice or likeness without
   explicit written consent. Use fictional characters, or actors who have
   consented and are on set. No face-swap. No deepfake. This is a hard rule,
   not a preference.
7. Composite in HyperFrames or Remotion: cut the footage to the beat, add
   kinetic type and captions on top, grade after the cut is locked. Do not
   grade before the cut.
8. Hand off to the editor with the best takes, clip file names, licences,
   and briefs used.

## Output format
- Shot briefs: one per shot, with source (supplied / stock / cloud API), file name, duration, fps
- Character lock: one paragraph, pasted into every brief
- Takes: 3 per shot, best take marked, flaws noted
- Realism check: hands, text, logos, physics — pass / fail per shot
- Licences: clip, source, licence, file name
- Consent notes: who is in the video, consent proof file name

## Quality bar
- A viewer cannot tell in the first 3 seconds that a shot is stock — or, if
  they can, it is clearly honest about it. Generic and unlabelled is a fail.
- Hands have the right number of fingers. Text in frame is spelled correctly.
- The product looks like the real product: colour, shape, label, size.
- Motion is smooth. No morphing faces, no melting objects.

## Examples
- Product in use: "Close-up, hands open a gold bangle box on a Diwali table, warm diya light, 9:16, 24fps, shallow depth of field." (Stock search: "hands gold bangle box diya light".)
- Street scene: "Wide, Mumbai street at dusk, family walks past lights, camera tracks slowly, warm practicals." (Stock search: "Mumbai street dusk family lights".)
- Demo: "Over-shoulder, phone screen shows 2-tap payment, finger taps twice, success tick, bright daylight." (Shoot it — a demo must be the real product.)

## Anti-patterns
- A 30-second single stock clip as the whole ad. Cut it into shots that serve the beats.
- Changing the character description between shots.
- Using a celebrity or a real influencer without consent.
- Using footage with unreadable or wrong text in frame and hoping no one reads it.
- A cloud API clip with a warped label or a wrong product. The product must be the real product — if the API cannot do that, use supplied footage instead.
- No licence note per clip. Every clip needs a source and a licence.

## Hard limits (see references/realistic-limits.md)
- No local GPU video model in this repo. Nothing here needs a GPU.
- Stock footage is generic by nature — it cannot show your exact product.
  For the product moment, shoot it or use supplied footage.
- Cloud video APIs are paid, third-party, and per-provider terms apply.
  A generated clip is not proof the product looks right — check it frame by frame.
- MoneyPrinterTurbo is prototyping and assembly only — never the paid hero ad,
  never its bundled music.

## References
- `references/realistic-limits.md` — Realistic-footage limits — stock, supplied footage, and paid cloud APIs, and what cannot run without a GPU.
- Read only the reference file for the step you are on; do not load every reference at once.
