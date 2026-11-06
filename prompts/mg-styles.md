# Motion-Graphic Styles — 15 Original Styles

All 15 styles are original, written for this repo. They follow the lemo
11-section style format (essence + what it is not, materials, colour logic,
type, motion, camera grammar, sound, native moves, pitfalls, engine,
variation) and the mg prompt template (style contract + creative seed +
signature features with checkable numbers + self-score).

Pick ONE style per ad. One style per ad — do not mix five styles.

## How to use a style

1. Read the style's 11 sections. The style is a contract, not a mood.
2. Write the treatment first, with the style's creative seed swapped for your
   ad's facts. Never rebuild a demo's story.
3. Prove the style: render a style frame first (real code), then a 10–15s
   demo film. A style with no rendered frame is a description, not a style.
   The one style proven end-to-end in this repo is the HyperFrames Diwali
   project in `examples/hyperframes-diwali-8s/` — use it as the proof pattern.
4. Keep a brand-owned version in your own folder (safe-to-change vs
   character-changing vs can't-change sections, style frame vs base
   side-by-side, CHANGES.md). Never edit the library style itself.

## Style index

| # | Style | Spec | Stack | Use for |
|---|---|---|---|---|
| 1 | Kinetic Pop | 15s, 30 fps, 9:16 | HyperFrames | Gen-Z, fintech, fast product |
| 2 | Smooth Premium | 15s, 30 fps, 9:16 | HyperFrames | Jewellery, premium, Diwali |
| 3 | Sticker Slam | 15s, 30 fps, 9:16 | HyperFrames | UGC, food, fun brands |
| 4 | Typewriter Truth | 15s, 24 fps, 9:16 | HyperFrames | Fintech, explainers, challenger |
| 5 | Slide & Reveal | 30s, 30 fps, 9:16 | Remotion | Product launch, steps, how-it-works |
| 6 | Bounce Lite | 15s, 30 fps, 9:16 | HyperFrames | Snacks, games, family |
| 7 | Fade & Glow | 30s, 24 fps, 9:16 | HyperFrames | Festive, night, premium |
| 8 | Whip Pan | 15s, 30 fps, 9:16 | HyperFrames | Fast cuts, street, sports |
| 9 | Split Screen | 30s, 30 fps, 9:16 | Remotion | Before/after, comparison |
| 10 | Hand-Drawn Sketch | 15s, 24 fps, 9:16 | HyperFrames | Education, local shops, warm brands |
| 11 | Neon Night | 15s, 30 fps, 9:16 | HyperFrames | Night, gaming, music |
| 12 | Paper Cut | 30s, 24 fps, 9:16 | HyperFrames | Gifting, Diwali, handmade |
| 13 | Zoom Punch | 15s, 30 fps, 9:16 | HyperFrames | One-line jokes, price reveals |
| 14 | Countdown | 10s, 30 fps, 9:16 | HyperFrames | Launches, offers, drops |
| 15 | Loopable Meme | 10s, 30 fps, 9:16 | HyperFrames | Reels / Shorts that loop |

Output spec for every style: 1080x1920, H.264 + stereo AAC 48 kHz, -14 LUFS
integrated, true peak below -1 dBTP. Deterministic render: every frame a pure
function of time, seeded randomness only, no timers, no network fetches.
Vertical numbers for every style: top 168px clear, text band 168–1330px,
min 28px type, about 5 words per claim line, frame 0 is the thumbnail.

---

## 1. Kinetic Pop

- **Essence:** words pop in one by one on the beat, small overshoot, then
  settle. Energy first, explanation second. **Not:** a slideshow, a wall of
  text, or decoration for its own sake.
- **Materials:** flat vector shapes, bold type, one product cut-out. No
  gradients, no stock photos, no 3D.
- **Colour logic:** black field, yellow #FFD400 as the only signal colour,
  white for body text. Only one thing carries the signal colour at a time;
  that thing is the protagonist.
- **Type:** one heavy display face, all caps for the punch, sentence case for
  the setup. Hook words at 9–12% of frame height.
- **Motion:** entrances `power4.out`, 0.3–0.5s; overshoot
  `cubic-bezier(0.34,1.56,0.64,1)`; stagger words 60–120ms; exits 40–50%
  shorter than entrances; next element starts at 30–50% of the previous one.
- **Camera grammar:** static frame; the type is the camera. One push-in on
  the product only, at second 10.
- **Sound:** one drum hit per word pop, silence between beats, a chime on the
  product landing. Cue map first; picture locks to the beat grid.
- **Native moves:** word-by-word pop; price slam; product drop-in with a
  small bounce that settles in 0.4s.
- **Pitfalls:** more than one pop at a time; pops faster than the viewer can
  read; a bounce that loops.
- **Engine:** HyperFrames, HTML + GSAP `fromTo`, one paused timeline per
  composition on `window.__timelines`. Fonts downloaded before rendering.
- **Variation:** 3 structures (pop-pop-payoff / question-answer-payoff /
  countdown-payoff), 3 openings (word / sound / face), 3 endings (CTA pill /
  price slam / logo whisper). **Banned:** particle explosions, RGB split,
  lens flare. **Self-score:** aim 9/10, fix the lowest dimension first.

## 2. Smooth Premium

- **Essence:** slow ease, gold shimmer, no bounce. The product is calm and
  expensive; the motion proves it. **Not:** fast, loud, or funny.
- **Materials:** cream paper, gold foil, deep maroon field, real product
  photography or supplied pack shots. No neon, no stickers.
- **Colour logic:** cream #FFF6E5 field, gold #D4A017 as the signal, deep
  maroon #7A1F2B as the anchor. Gold is reserved for the product and the price.
- **Type:** an elegant serif for the hook, a clean sans for captions. Hook at
  8–10% of frame height, generous leading.
- **Motion:** entrances `expo.out`, 0.6–0.9s; no bounce, no spin, only ease.
  Text holds 0.5s + 0.3s per word; last line holds at least 2s.
- **Camera grammar:** slow push-in throughout, one speed, no cuts for the
  first 6 seconds. The camera breathes; it never whips.
- **Sound:** one soft string note per beat, a low drone under the payoff,
  silence before the price. -14 LUFS, true peak below -1 dBTP.
- **Native moves:** gold shimmer travelling across the product; a slow reveal
  from behind a maroon panel; the price fading in like a hallmark stamp.
- **Pitfalls:** fades that are too slow to read; gold that looks like yellow
  plastic; a shimmer that loops and distracts.
- **Engine:** HyperFrames, HTML + GSAP `fromTo`. Proven pattern:
  `examples/hyperframes-diwali-8s/` uses this style's palette and pacing.
- **Variation:** 3 structures (reveal / ritual / homecoming), 3 openings
  (diya / hands / doorway), 3 endings (price / store / blessing).
  **Banned:** bounce easing, particle explosions, neon glow.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 3. Sticker Slam

- **Essence:** stickers slam in with a small shake, then stick. One sticker
  per beat. Playful, handmade, a little messy on purpose. **Not:** polished
  or corporate.
- **Materials:** die-cut sticker shapes, thick white borders, flat colour,
  one real photo cut-out. Paper texture, no gradients.
- **Colour logic:** white field, pink as the signal, black for outlines and
  type. Three colours max.
- **Type:** one chunky rounded display face, mixed case, slightly rotated
  (2–4 degrees) for the handmade feel.
- **Motion:** slam in with a 0.15s shake, then stick. One sticker per beat,
  never two. Squash about 10% on landing.
- **Camera grammar:** static frame; stickers do the moving. One zoom on the
  punch sticker only.
- **Sound:** a paper slap per sticker, a giggle or pop on the payoff.
- **Native moves:** sticker peel (corner lifts, then sticks); sticker stack
  (three stickers land on each other); sticker wobble (one wobble, then still).
- **Pitfalls:** stickers that keep moving after landing; more than one sticker
  per beat; a shake that reads as a glitch.
- **Engine:** HyperFrames, HTML + GSAP `fromTo`, `back.out(1.4)` for the slam.
- **Variation:** 3 structures (slam-slam-payoff / peel-reveal / stack-and-topple),
  3 openings (one sticker / a hand / a sound), 3 endings (CTA sticker /
  price sticker / joke sticker). **Banned:** RGB split, lens flare, neon glow.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 4. Typewriter Truth

- **Essence:** text types on, letter by letter, with a cursor blink. The
  truth arrives one letter at a time, and the pause on the punch line is the
  joke. **Not:** a paragraph on screen, or a voiceover reading a document.
- **Materials:** black field, white type, one hero colour for the punch word.
  No images until the payoff.
- **Colour logic:** black #111111 field, white body, hero colour reserved for
  the one word that matters. That word is the only colour on screen.
- **Type:** one monospace face for the typing, one heavy display face for the
  punch word. Typing speed matches speech: about 15 letters per second.
- **Motion:** letters appear one by one, cursor blinks, the line holds
  0.5s + 0.3s per word after the last letter. No other motion while typing.
- **Camera grammar:** static. The cursor is the only movement. One cut to
  the product on the payoff.
- **Sound:** a soft key click per letter, silence on the punch hold.
- **Native moves:** the reveal (the punch word types in a different colour);
  the delete (a wrong line deletes itself, then the true line types on);
  the pause (the cursor blinks three times, then the payoff lands).
- **Pitfalls:** typing faster than speech; a wall of text; a cursor that
  never stops blinking.
- **Engine:** HyperFrames, HTML + GSAP. Type is DOM text, never an image.
- **Variation:** 3 structures (claim-proof / wrong-right / question-answer),
  3 openings (a question / a number / a lie), 3 endings (CTA / price /
  one-word payoff). **Banned:** particle explosions, bounce easing.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 5. Slide & Reveal

- **Essence:** panels slide in from one side, revealing the next beat. One
  direction only. The ad is a corridor, not a collage. **Not:** slides from
  every direction, or a carousel.
- **Materials:** brand hero colour panels, white type panels, one product
  panel. Flat, no shadows except one soft edge.
- **Colour logic:** hero colour for the panels, white for type, dark for the
  final panel. The final panel is always the darkest — it holds the CTA.
- **Type:** one display face, left-aligned, large. Numbers at 12% of frame
  height for step numbers.
- **Motion:** panels slide in from the right, `power4.out`, 0.5s, stagger
  80ms. One direction, no reverse slides. Exits 40–50% shorter.
- **Camera grammar:** the panels are the camera. One slow push-in on the
  final panel only.
- **Sound:** one soft whoosh per panel, a chime on the final panel.
- **Native moves:** the wipe (a panel covers the old beat); the step reveal
  (a number slides in, then its line); the merge (two panels become one for
  the payoff).
- **Pitfalls:** sliding from two directions; panels that overlap the text
  band; a reveal that is faster than the read.
- **Engine:** Remotion (React, JSON inputProps for steps) or HyperFrames.
  Remotion is the natural fit: steps are data, not a re-edit.
- **Variation:** 3 structures (3 steps / problem-solution / before-after),
  3 openings (a question panel / a number / a face), 3 endings (CTA panel /
  price panel / logo panel). **Banned:** RGB split, lens flare.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 6. Bounce Lite

- **Essence:** elements bounce in once, lightly, then settle. Good for kids,
  snacks, and family brands. Joyful, never frantic. **Not:** a trampoline,
  or a loop.
- **Materials:** bright flat shapes, rounded corners, one product cut-out.
  Three colours max.
- **Colour logic:** bright field, one hero colour, white. The hero colour is
  the product's colour.
- **Type:** one rounded display face, sentence case, large.
- **Motion:** bounce in once with `back.out(1.2)`, settle in 0.5s. Bounce
  once, never loop. Squash about 10% on landing.
- **Camera grammar:** static frame, one gentle push-in on the payoff.
- **Sound:** a soft boing per bounce, a giggle on the payoff.
- **Native moves:** the drop (an element drops in and bounces once); the
  hop (the product hops across the frame); the settle (everything lands and
  goes still for the CTA).
- **Pitfalls:** bouncing more than once; bouncing while the text is being
  read; a bounce that reads as a glitch.
- **Engine:** HyperFrames, HTML + GSAP `fromTo`.
- **Variation:** 3 structures (drop-payoff / hop-hop-payoff / settle-and-say),
  3 openings (a drop / a hop / a sound), 3 endings (CTA / price / giggle).
  **Banned:** bounce easing on text (use it on objects only), particle
  explosions. **Self-score:** aim 9/10, fix the lowest dimension first.

## 7. Fade & Glow

- **Essence:** elements fade in with a soft glow, hold, fade out. Slow and
  calm. Night, festive, premium. **Not:** fast, or a slideshow with music.
- **Materials:** deep blue field, gold light, cream type. Soft glow, no hard
  edges. One diya, one face, or one product — never all three at once.
- **Colour logic:** deep blue anchor, gold #D4A017 as the only light, cream
  for type. The glow is the protagonist.
- **Type:** one elegant serif, generous leading, slow fades.
- **Motion:** fades are 0.8s, not instant. Holds 0.5s + 0.3s per word.
  Exits are fades, 40–50% shorter than entrances.
- **Camera grammar:** static or one very slow push-in. The glow moves, the
  camera does not.
- **Sound:** a low drone, one chime per fade-in, silence before the payoff.
- **Native moves:** the glow reveal (light travels across the product); the
  diya (a flame fades in and steadies); the ember (one warm dot grows into
  the CTA).
- **Pitfalls:** fades so slow the viewer swipes; a glow that blooms the whole
  frame; text that fades in and out before it can be read.
- **Engine:** HyperFrames, HTML + GSAP `fromTo` on opacity only.
- **Variation:** 3 structures (dark-light / night-morning / one-flame),
  3 openings (darkness / a dot / a face), 3 endings (CTA / blessing / price).
  **Banned:** strobing, particle explosions, neon glow.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 8. Whip Pan

- **Essence:** whip pan between beats, fast blur, then a sharp hold. One whip
  per beat change. Speed is the joke. **Not:** a whip every second, or a
  blur that never resolves.
- **Materials:** bold type, hard light, street or sports footage (supplied
  or licensed stock, composited in HyperFrames). No soft focus.
- **Colour logic:** black, white, one hero colour. High contrast; the whip
  is visible because the colours are.
- **Type:** one heavy display face, all caps, short lines only.
- **Motion:** whip 0.25s with motion blur (`data-motion-blur="on"`), then a
  sharp hold of at least 1.5s. Whip only on a beat change.
- **Camera grammar:** the whip IS the camera. Between whips, the frame is
  static and the subject is centred.
- **Sound:** a whoosh per whip, a beat drop on the hold.
- **Native moves:** the whip reveal (the next beat arrives on the whip); the
  whip cut (the whip carries the cut, no fade); the whip stop (a whip that
  stops dead on the product).
- **Pitfalls:** whipping so fast the text is unreadable; whipping without a
  hold; a whip that reads as a mistake.
- **Engine:** HyperFrames, HTML + GSAP `fromTo` on a wrapper, never on a
  `.clip` itself.
- **Variation:** 3 structures (whip-whip-payoff / chase / race), 3 openings
  (a run / a shout / a door), 3 endings (CTA / price / freeze frame).
  **Banned:** fades, particle explosions. **Self-score:** aim 9/10, fix the
  lowest dimension first.

## 9. Split Screen

- **Essence:** the screen splits into two, each side tells one side of the
  story, then merges for the payoff. Comparison made visible. **Not:** two
  ads at once, or a split that never merges.
- **Materials:** two contrasting colours, white type, one product. Two
  supplied or licensed images at most — one per side.
- **Colour logic:** two contrasting colours, one per side, white for type.
  The merge panel is the hero colour.
- **Type:** one display face, mirrored layout, same size both sides.
- **Motion:** split once, 0.5s, `power4.out`. Each side moves independently
  for 3–4 seconds. Merge once for the payoff, 0.6s.
- **Camera grammar:** static both sides; the split line is the only vertical.
  The merge is a slow push-in.
- **Sound:** two sounds, one per side, that resolve into one chord on the merge.
- **Native moves:** the split (one frame becomes two); the mirror (both sides
  do the same action differently); the merge (two stories become one product).
- **Pitfalls:** splitting more than once; sides that are not actually
  different; a merge with no payoff.
- **Engine:** Remotion (React, two compositions side by side) or HyperFrames.
- **Variation:** 3 structures (before-after / two characters / two choices),
  3 openings (one frame / a question / a face), 3 endings (merge-CTA /
  merge-price / merge-joke). **Banned:** RGB split, lens flare.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 10. Hand-Drawn Sketch

- **Essence:** lines draw themselves, then fill with colour. Imperfect,
  human, warm. **Not:** a polished vector ad, or a whiteboard lecture.
- **Materials:** paper cream field, ink black lines, one accent colour.
  Lines boil slightly (reseeded, never jittery) for the handmade feel.
- **Colour logic:** paper cream, ink black, one accent. The accent is the
  product's colour, and only the product gets it.
- **Type:** one hand-lettered style face for the hook, one clean sans for
  captions. Never more than two faces.
- **Motion:** lines draw at a readable speed — a line takes as long as it
  takes to say the word it draws. Fill arrives after the line, never before.
- **Camera grammar:** static frame; the drawing is the movement. One slow
  push-in on the finished drawing.
- **Sound:** a pencil scratch per line, a soft chime when the fill lands.
- **Native moves:** the draw-on (a line draws the product); the fill (colour
  washes in from one corner); the correction (a line is redrawn, better —
  the imperfection is the charm).
- **Pitfalls:** drawing faster than the viewer can follow; a fill that
  arrives before the line; lines so wobbly they read as a mistake.
- **Engine:** HyperFrames, HTML + Canvas or SVG stroke animation, deterministic
  `seek(t)`. No CSS transitions.
- **Variation:** 3 structures (draw-reveal / draw-fix / draw-story), 3 openings
  (a blank page / a hand / a dot), 3 endings (CTA / signature / price).
  **Banned:** particle explosions, neon glow, bounce easing.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 11. Neon Night

- **Essence:** neon text flickers on, holds, flickers off. Product glows.
  Night, gaming, music. **Not:** a strobe, or a cyberpunk cliche.
- **Materials:** black field, neon pink and neon cyan type, one product with
  a soft glow. No gradients, no lens flare.
- **Colour logic:** black anchor, neon pink as the signal, neon cyan as the
  second voice. Only two neons, never three.
- **Type:** one bold display face, all caps, large. The flicker is the type.
- **Motion:** flicker once, then hold steady — no strobing. Flicker is 0.2s,
  hold is at least 2s. Text holds 0.5s + 0.3s per word.
- **Camera grammar:** static frame; the flicker is the movement. One slow
  push-in on the product.
- **Sound:** a buzz on the flicker, a bass note on the hold.
- **Native moves:** the flicker-on (text flickers once, then holds); the
  glow (the product glows once, then steadies); the sign-off (the neon
  turns off line by line, leaving the CTA).
- **Pitfalls:** strobing (never flash at 3 per second or more); a flicker
  that never settles; neon on neon (unreadable).
- **Engine:** HyperFrames, HTML + GSAP `fromTo` on opacity. No CSS filters.
- **Variation:** 3 structures (flicker-hold / sign-on / sign-off), 3 openings
  (dark / a buzz / a face), 3 endings (CTA / price / lights-out).
  **Banned:** strobing, lens flare, particle explosions.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 12. Paper Cut

- **Essence:** paper layers slide and lift, with soft shadows. Tactile,
  crafted, handmade. **Not:** a flat slideshow, or a craft fair.
- **Materials:** paper tones, one hero colour, soft shadows. Layers are
  real shapes with depth, not images of paper.
- **Colour logic:** paper tones for the field, one hero colour for the
  product layer. The top layer is always the hero colour.
- **Type:** one serif face for the hook, one clean sans for captions.
- **Motion:** layers slide and lift slowly, `power4.out`, 0.6–0.9s. Shadows
  are soft, movement is slow. One layer moves at a time.
- **Camera grammar:** a slight top-down angle; the layers lift toward the
  viewer. One slow push-in on the final layer.
- **Sound:** a paper rustle per layer, a soft thud when a layer lands.
- **Native moves:** the lift (a layer lifts to reveal the next); the fold
  (a layer folds back like a card); the stack (layers stack into the product).
- **Pitfalls:** layers that move too fast to feel like paper; shadows so hard
  they read as dirt; more than one layer moving at once.
- **Engine:** HyperFrames, HTML + GSAP `fromTo`. Shadows are CSS box-shadows
  on children, never on a `.clip`.
- **Variation:** 3 structures (lift-reveal / fold-story / stack-payoff),
  3 openings (a flat page / a hand / a gift), 3 endings (CTA / gift /
  price). **Banned:** particle explosions, neon glow, bounce easing.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 13. Zoom Punch

- **Essence:** the camera zooms in on the punch word, then cuts to product.
  One zoom per ad. The zoom is the joke. **Not:** a zoom every beat, or a
  slow drift.
- **Materials:** white field, black type, one hero colour. One product shot
  (supplied or licensed).
- **Colour logic:** white field, black type, hero colour reserved for the
  punch word. The punch word is the only colour until the product appears.
- **Type:** one heavy display face, the punch word at 12–15% of frame height.
- **Motion:** one zoom, 0.4s, `power4.in`, on the punch word only. Then a
  hard cut to the product. Zoom once, at the punch.
- **Camera grammar:** the zoom IS the camera. Everything else is static.
- **Sound:** silence, then a single hit on the zoom, then the product sound.
- **Native moves:** the zoom (in on the punch word); the cut (hard cut to
  product, no fade); the hold (product holds still for 2–3 seconds).
- **Pitfalls:** zooming twice; zooming on the wrong word; a zoom so slow it
  reads as a drift.
- **Engine:** HyperFrames, HTML + GSAP `fromTo` on scale, `transform-origin`
  on the punch word.
- **Variation:** 3 structures (setup-zoom-payoff / question-zoom-answer /
  price-zoom), 3 openings (a word / a face / a number), 3 endings (CTA /
  price / product hold). **Banned:** fades, particle explosions.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 14. Countdown

- **Essence:** numbers count down 3-2-1, then the product lands. Fast,
  tense, then release. **Not:** a timer on screen for 10 seconds, or a
  countdown with no payoff.
- **Materials:** black field, white numbers, one red accent. Numbers are
  the visual — nothing else moves while they count.
- **Colour logic:** black anchor, white numbers, red accent for the final
  number only. Red appears once.
- **Type:** one heavy display face, numbers at 20% of frame height.
- **Motion:** numbers change on the beat, 1 second each, countdown is 3
  seconds max. The product lands on the beat after 1, with a 0.4s settle.
- **Camera grammar:** static frame; the numbers are the movement. One
  push-in on the product after the countdown.
- **Sound:** a tick per number, a boom on the product landing.
- **Native moves:** the count (3-2-1, one second each); the landing (the
  product drops in on the beat); the hold (price holds 2 seconds).
- **Pitfalls:** a countdown longer than 3 seconds; numbers that change off
  the beat; a product that lands late.
- **Engine:** HyperFrames, HTML + GSAP. Numbers are DOM text, timed to the
  cue map.
- **Variation:** 3 structures (countdown-launch / countdown-offer /
  countdown-drop), 3 openings (a number / a face / a door), 3 endings (CTA /
  price / sold-out). **Banned:** particle explosions, lens flare.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## 15. Loopable Meme

- **Essence:** the last frame matches the first frame, so the loop is
  seamless. The joke repeats. **Not:** a video that ends, or a loop with a
  visible cut.
- **Materials:** bold flat shapes, two colours, one joke. The joke is one
  line and one action.
- **Colour logic:** bold field, two colours only. The second colour is the
  punch.
- **Type:** one heavy display face, one line only.
- **Motion:** the action returns to its start state by the last frame.
  Test the loop 3 times — if the cut is visible, fix it. Loop seam is
  checked on neighbouring frames, not on a single still.
- **Camera grammar:** static frame. The loop is the movement.
- **Sound:** a looped beat, one sound per cycle, first frame equals last
  frame in audio too.
- **Native moves:** the return (the hero ends where they started); the
  repeat (the joke lands, then lands again); the seamless cut (the cut
  hides inside the motion).
- **Pitfalls:** a visible cut; a joke that only works once; a loop that
  drifts by one frame per cycle.
- **Engine:** HyperFrames, HTML + GSAP, deterministic `seek(t)` — the first
  and last frames must be identical by construction, not by editing.
- **Variation:** 3 structures (action-return / joke-repeat / cycle), 3 openings
  (mid-action / a word / a face), 3 endings (same as the opening — that is
  the point). **Banned:** fades, particle explosions.
  **Self-score:** aim 9/10, fix the lowest dimension first.

## How to choose

- Gen-Z / fast: Kinetic Pop, Sticker Slam, Whip Pan, Zoom Punch, Loopable Meme.
- Premium / festive: Smooth Premium, Fade & Glow, Paper Cut.
- Challenger / explain: Typewriter Truth, Slide & Reveal, Split Screen.
- One style per ad. Do not mix. Test the 3-second hook before the full render.
- Own your style: safe-to-change vs character-changing vs can't-change
  sections, style frame vs base side-by-side, CHANGES.md, keep in your folder.
