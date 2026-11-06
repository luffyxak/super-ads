---
name: ad-video-director
description: >-
  Direct shots, camera, performance, and sound for a 15-30 second ad, and write the prompt brief for every shot. Use when you have a script and styleframes and need a shot list, when a shoot or a generation feels flat, when sound is an afterthought, or when a product moment needs staging. Trigger phrases: 'write the shot list', 'direct this scene', 'plan the sound', 'the shots feel flat'. Delivers a shot list and director notes. Do NOT use for animating the shots — hand off to the animator.
license: MIT
---
# Ad Video Director

## When to use
- After script + styleframes, before shooting or generating video.
- When the ad is a series of pretty shots with no performance.
- When sound is an afterthought.

## Workflow
1. Read the script beat by beat. Turn each beat into 1–3 shots. 15s is 5–8 shots.
   30s is 10–14 shots. More shots is not better. Better shots is better.
2. For each shot, write: shot size, camera move, action, line, sound, duration.
   Use the shot-list template in `templates/shot-list.csv`.
3. Direct performance: one clear action per shot. Deadpan beats shouting for challenger ads.
   Warm and real beats polished for festive / family ads.
4. Plan sound from the start: music, sound effects, silence. Silence is a choice.
   A beat with no music can be the funniest beat.
5. Plan the product moment: the product appears once, clearly, in good light, for 2–3 seconds.
   Not a 10-second pack shot. Show it in use, not on a pedestal.
6. Plan transitions: match cuts, whip pans, jump cuts. One transition style per ad.
   Do not use a different transition every shot.
7. Write director notes: what the actor should feel, what the camera should feel,
   what the audience should feel — in one line each.
8. Hand off to the animator / editor with shot list + director notes.

## Output format
- Shot list: shot number, time, size, camera, action, line, sound, duration
- Director notes: performance, camera, audience feeling — one line each
- Sound plan: music, effects, silence — where each starts and stops
- Product moment: shot number, time, how it is shown

## Quality bar
- Every shot earns its seconds. If you can cut it and nothing is lost, cut it.
- The camera moves for a reason. No movement for decoration.
- Performance is specific: what is the actor trying to do in this shot?
- Sound-off still works. Sound-on is better.

## Examples
- 15s reel: Shot 1 — close-up, hook line, deadpan. Shot 2 — wide, chaos. Shot 3 — product in hand, 2 seconds.
- Diwali: Shot 1 — diya close-up. Shot 2 — family wide. Shot 3 — hands exchanging a box. Shot 4 — gold close-up.
- Fintech: Shot 1 — actor angry at a form. Shot 2 — phone, 2 taps, done. Shot 3 — actor calm, smiling.

## Anti-patterns
- A shot list that is just "various shots of product".
- Actors shouting the brand name. Let the idea shout.
- Music that starts loud and stays loud for 30 seconds.
- A product shot that looks like a catalogue, not a moment.

## References
- `references/shot-language.md` — Shot language and the 9-part prompt anatomy for code-rendered and realistic shots.
- Read only the reference file for the step you are on; do not load every reference at once.
