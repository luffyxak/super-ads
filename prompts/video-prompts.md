# Video Prompts — Original Prompts in Three Tiers

All prompts here are original, written for this repo. Patterns were learned
from prompt-library repos; no prompt text was copied from them.

## Two routes — pick the right one first

- **Code-rendered (default for this repo):** motion graphics made by a coding
  agent — HTML/Canvas/SVG + GSAP, HyperFrames, or Remotion. Motion graphics is
  the dominant ad form in the research (71.6% of ad/launch files). Deterministic,
  versionable, renders on this machine. Prompts in Tiers 1–3 are for this route.
- **Realistic footage (labelled below):** client-supplied clips or licensed stock,
  composited in HyperFrames/Remotion — or, optionally, one shot from a paid cloud
  video API. No local GPU model in this repo. Use when you cannot shoot the scene.

## Prompt anatomy — the 9 parts of a prompt that renders well

1. Duration, scene count, one beat per scene — storyboard first, code second.
2. Assets supplied, by name — real product, reference image, music, font, colours.
3. Renderer and stack named — HyperFrames, Remotion, or a realistic-footage route (stock / supplied / paid cloud API).
4. Camera and motion language — named moves with timing, not adjectives.
5. Deterministic rendering rule — every frame a pure function of time; seeded
   randomness only; no CSS transitions, no timers, no state between frames.
6. Banned list — the cliches that make output look templated.
7. Audio and text spec — music on or off, TTS voice and language, caption
   language and safe zone.
8. Self-check — render keyframes first, inspect overlap, crowding, legibility.
9. Effort and tools — Node 20+, Chrome, ffmpeg 7+, keys in .env, never read by the agent.

## Banned list (applies to every prompt in this file)

Particle explosions, RGB split, lens flare, neon glow, bounce easing,
generic piano-and-strings music, a logo card as the opening frame.
If the output looks templated, the banned list is the first thing to check.

## Cost and iteration

Budget 2+ rounds. A one-liner costs minutes and a few dollars; a full spec
costs about an hour and tens of dollars. One prompt does not equal one ad —
expect a make, review, revise loop, scored by a second AI jury.

---

## Tier 1 — One-line triggers (code-rendered)

One sentence: product + tone + format. The model invents everything else.
Works when the idea is simple and the skill library behind it is prepared.

1. "Make a punchy 15-second vertical launch film for a mango sparkling water — bright, fast, one joke, product lands in the last 3 seconds. HyperFrames, 1080x1920, 30 fps."
2. "Make a warm 15-second Diwali reel for gold bangles — family, one diya, the gift ends a small argument. HyperFrames, 9:16, 30 fps, Hinglish captions on."
3. "Make a deadpan 30-second fintech ad: a serious man, a paper form, two taps, he relaxes. Moonshot energy, 9:16, 24 fps, no music on the joke beat."
4. "Make a 10-second countdown launch for a new snack — numbers 3-2-1, product lands, one price line holds 2 seconds. 9:16, 30 fps."
5. "Make a 15-second kinetic-type ad for a no-making-charge gold offer — words pop on the beat, bangles slide in at 10 seconds, CTA holds 3 seconds. 9:16."
6. "Make a 15-second UGC-style ad for a drink in a kitchen — creator tastes it, laughs, holds the can to camera. Handheld feel, captions on, 30 fps."

## Tier 2 — Fill-in templates (code-rendered)

A fixed skeleton with slots. Same structure every time, different facts.

### Template A — 30-second explainer
"30-second explainer, 3 scenes: [problem] → [how it works] → [price + CTA].
Brand colours [___], Hinglish voiceover, captions on, 9:16, 24 fps. HyperFrames.
Deterministic render, seeded randomness only. Banned: particle explosions, RGB split.
Self-check: render keyframes at 0, 8, 20, 28 seconds first."

### Template B — 15-second product launch
"15-second launch reel for [product]. Hook in second 1–2. The product appears
once, clearly, in use, for 2–3 seconds. No hard sell before 80%. CTA in the last
3 seconds: [CTA]. About 35 words. 9:16, 30 fps. Captions for every line."

### Template C — Diwali reel
"15-second Diwali reel for [brand]. Ritual: [diya lighting / gift exchange /
first gold purchase]. Family tension: [one line]. Product is the guest, not the
host. Offer: [what, how much, till when, where] with proof. Hinglish, warm,
Tier-2/3 clarity. 9:16, 30 fps, captions on."

### Template D — Price reveal
"Price reveal for [product] at ₹[price]. The price appears once, big, clear,
for 2 seconds, at the payoff. No 'up to', no asterisk without the real number
in the same frame. 15 seconds, 9:16, 30 fps, captions on."

## Tier 3 — Full spec (code-rendered, mg prompt template)

A full spec is a production brief, not a wish. Use the mg template:
role + quality bar, fixed output spec, tech route, creative seed, signature
features with checkable numbers, how-to-work, rules, craft checklist +
self-score, deliver + report.

### Spec 1 — Diwali gold bangles, 15s, HyperFrames
"Role: you are a motion designer for a premium Indian jewellery brand.
Quality bar: high-end agency work, rewatchable, meme-able.
Output: 1080x1920, 30 fps, exactly 15.000s, H.264 + stereo AAC 48 kHz,
-14 LUFS integrated, true peak below -1 dBTP.
Tech route: HyperFrames, HTML + GSAP (fromTo only, paused timelines on
window.__timelines), vendored GSAP, fonts downloaded before rendering.
Creative seed — beats: 0–2s hook, gold words pop on the beat, one diya flame;
2–6s setup, hands lift bangles from a maroon box, slow push-in; 6–12s twist,
family at the door with diyas, camera tracks in; 12–15s payoff, product lockup
gold on cream, CTA 'Shop Now' holds 3s. Palette: deep maroon #7A1F2B, gold
#D4A017, cream #FFF6E5. Sound: warm tabla at 96 BPM, one chime on the reveal.
Signature features (checkable): hook words appear one by one, stagger 2–4
frames; entrances use power4.out, exits 40–50% shorter; text holds 0.5s +
0.3s per word; last line holds at least 2s; top 168px clear, text band
168–1330px, min 28px type.
How to work: treatment first, then keyframes at 0, 2, 6, 12, 14 seconds,
then motion, then sound locked to the cue sheet, then final spec check.
Rules: deterministic — every frame a pure function of time, seeded randomness
only, no timers, no network fetches; assets only OFL / CC0 / free for
commercial use, recorded in CREDITS.md; no real brand trademarks.
Craft checklist + self-score: score 1–10 on hook, timing, type, motion,
sound, brand, rewatchability; aim for 9, fix the lowest first.
Deliver: video.mp4 + a short report (concept, beat sheet, how each signature
feature is realised, tech route, check numbers, honest top-3 weaknesses)."

### Spec 2 — Fintech deadpan, 30s, HyperFrames
"Role: you are a comedy director in the Moonshot school. Quality bar: the joke
is the ad, the brand is the punchline's excuse.
Output: 1080x1920, 24 fps, exactly 30.000s, -14 LUFS.
Tech route: HyperFrames, HTML + GSAP, kinetic type for the two-tap demo.
Creative seed — beats: 0–2s hook, a serious man stares at a paper bank form;
2–8s setup, the form grows taller, he gets angrier; 8–20s twist, he taps a
phone twice and the form shrinks to nothing; 20–27s payoff, he relaxes, deadpan
line; 27–30s CTA, product + 'UPI in 2 taps' holds 3s. Palette: black #111111,
yellow #FFD400, white. Sound: silence on the joke beat, one soft tick per tap.
Signature features: one punch per beat; the form is the only thing that moves
big; type pops with overshoot cubic-bezier(0.34,1.56,0.64,1); squash about 10%.
Rules: deterministic render; no celebrity likeness; no real bank branding.
Self-score 1–10 on seven dimensions; fix the lowest first.
Deliver: video.mp4 + report with top-3 weaknesses."

### Spec 3 — Product launch, 10s, Remotion
"Role: you are a launch-film designer. Output: 1080x1920, 30 fps, exactly
10.000s, -14 LUFS. Tech route: Remotion, React + JSON inputProps so the price
and city can be swapped per version. Creative seed: the product is missing for
7 seconds, everyone looks for it, then it appears in the hero's hand at 7s,
camera pushes in, price appears once at 8s and holds 2s. Signature features:
one hero moves at a time; element-driven transitions (the product carries the
cut); loop seam tested — first frame equals last frame. Rules: deterministic;
invent the brand name, no real trademarks. Deliver: video.mp4 + report."

---

## Reference-led and real-asset prompts (code-rendered)

### Reference-led
"Using the attached pack shot as the only product reference, rebuild it as a
flat line-art animation; keep the label exactly as supplied, do not redraw
the logo. 15s, 9:16, 30 fps, HyperFrames."

### Real assets
"Animate the supplied app screenshots into a 15s promo: screenshot 1 slides in
at 0s, tap 1 at 4s, success tick at 8s. Use only the supplied frames; do not
regenerate the UI. 9:16, 30 fps, captions on."

### Director + cloud video API
"Director brief: 15s Diwali ad, 3 shots, warm home, gold close-up, family
payoff. Shot 2 prompt: [subject, action, camera, light, negative] — 9:16,
24 fps. Optional paid cloud route only — one shot at a time, paid, third-party terms apply; check the clip frame by frame."

---

## Realistic-footage shot briefs (LABELLED — supplied/licensed stock or optional paid cloud API)

One brief = one shot. Each brief below is a shot description for finding a
stock clip, directing a supplied clip, or (optionally) ordering one paid cloud
API shot. Stock is generic — it cannot show your exact product. For the product
moment, shoot it or use supplied footage. Never use a real person without
explicit written consent. Lock character, wardrobe, and light across shots.
Get 3 candidate clips or takes per shot and pick the best.

How to write one: subject, action, camera, light, style, negative.

1. Product launch — hero reveal: "9:16 vertical, studio, a mango sparkling
   water can rotates slowly on a white pedestal, condensation drops, soft
   daylight, camera dollies in slowly, 24fps, clean premium look. Negative:
   no text in frame, no extra cans, no warped label."
2. Diwali — homecoming: "9:16 vertical, warm Indian home at dusk, a young
   woman enters with a gift box, diyas glow on the windowsill, family turns
   and smiles, camera tracks with her, warm practical light, 24fps, cinematic,
   real skin tones. Negative: no fireworks, no warped faces, no extra fingers."
3. Diwali — gold close-up: "9:16 vertical, extreme close-up, hands lift gold
   bangles from a maroon velvet box, gold catches diya light, shallow depth of
   field, slow camera push-in, 24fps, premium jewellery look. Negative: no
   plastic-looking gold, no text, no morphing."
4. Fintech — Moonshot-style deadpan: "9:16 vertical, office, a serious man in
   a shirt stares at a paper bank form, deadpan, hard daylight, static camera,
   then he taps a phone twice and relaxes, 24fps, dry comedy, no music.
   Negative: no shouting, no warped phone screen, no extra fingers."
5. Fintech — 2-tap demo: "9:16 vertical, over-shoulder, phone screen shows a
   payment app, a finger taps twice, a green success tick appears, bright
   daylight, static camera, 24fps, clear UI, no glare. Negative: no warped
   text, no unreadable numbers, no morphing."
6. Food delivery — small order: "9:16 vertical, street at dusk, a delivery
   partner hands one small sweet box to an elderly woman, both smile, warm
   street light, camera holds wide then pushes in, 24fps, warm and human.
   Negative: no fast cuts, no warped faces."
7. Fashion — street walk: "9:16 vertical, city street, a young woman walks
   toward camera in a bright jacket, wind moves her hair, camera tracks
   backwards slowly, golden hour, 24fps, editorial fashion. Negative: no
   warped limbs, no morphing background."
8. Travel — mountain morning: "9:16 vertical, mountain viewpoint at sunrise,
   a traveller opens their arms, mist moves slowly, drone-like slow push-in,
   cool morning light, 24fps, epic but calm. Negative: no warped horizon,
   no extra people."
9. Beauty — mirror moment: "9:16 vertical, bathroom mirror, a woman applies a
   cream, smiles at herself, soft window light, close-up, slow push-in, 24fps,
   real skin texture, no retouching look. Negative: no plastic skin, no warped
   mirror, no text."
10. Auto — night drive: "9:16 vertical, city at night, a car drives through wet
    streets, reflections on the road, camera tracks low and slow, neon light,
    24fps, cinematic, premium. Negative: no warped wheels, no unreadable
    plates, no morphing."
11. Festive — neighbourhood sweets: "9:16 vertical, Indian lane at dusk,
    neighbours exchange sweet boxes, children run past with sparklers in the
    background, warm practical light, camera holds wide, 24fps, festive and
    warm. Negative: no fireworks close to faces, no warped hands."
12. UGC — creator in kitchen: "9:16 vertical, home kitchen, a creator in an
    apron tastes a drink, laughs, holds the can to camera, natural window
    light, handheld camera, 30fps, authentic UGC feel, captions space at
    bottom. Negative: no studio look, no warped label, no extra people."

## Consistency lock — paste into every realistic prompt for the same ad

"Character: [name, age, hair, wardrobe, skin tone — one paragraph]. Light:
[warm diya / hard daylight / soft studio]. Camera: 9:16, 24fps,
[static / slow push-in]. Style: [cinematic / deadpan / UGC]."
If the face changes between shots, the ad breaks. Regenerate with the same
seed and lock. For code-rendered ads, consistency is structural instead —
deterministic render(t), shared palette and type files — not a pasted paragraph.
