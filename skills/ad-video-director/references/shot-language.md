# Shot language — reference for ad-video-director

## Shot sizes and moves
Close-up for the hook and the product moment; wide for chaos and family;
tracking for entrances; static for deadpan. One camera move per shot, and the
move must have a reason. 15 seconds is 5-8 shots; 30 seconds is 10-14.

## Prompt anatomy (9 parts, for every shot prompt)
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

## Prompt tiers
- One-line trigger: product + tone + format; the model invents the rest.
- Fill-in template: fixed skeleton, slots for brand, product, price, language.
- Full spec: duration, scene count, one beat per scene, camera per beat, then code.
Use the tier that matches how much the human has already decided.

## Sound
Plan sound from the start: music, effects, silence. Silence is a choice.
A beat with no music can be the funniest beat. Voice is TTS plus an ASR check;
music is scored from the cue map; mix to -14 LUFS, true peak below -1 dB.
