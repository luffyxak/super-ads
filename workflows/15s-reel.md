# Workflow: 15s Reel

## Goal
One 15-second vertical reel that hooks in 2 seconds, lands one punch, and is rewatchable.

## Time estimate
- Strategy + concepts: 45 minutes
- Script + captions: 30 minutes
- Styleframes + shot list: 45 minutes
- Shoot / generate + motion: 2–3 hours
- Edit + export + QA: 1 hour
- Total: 4–5 hours for a first version, faster on version 2.

## Agents involved
Strategist → Creative Director → Copywriter → Visual Designer → Video Director → Animator → Editor → QA / Brand Safety

## Skills to load
- ad-strategy, ad-creative-director, ad-copywriter-gen-z
- ad-visual-designer, ad-video-director, ad-animation-motion
- ad-social-formats, ad-brand-safety

## Steps
1. Scaffold the brief: `python3 scripts/new_ad.py --brand X --product Y --format reel15 --festival none`
   Fill `outputs/<slug>/brief.md`. Do not start creative work with blanks.
2. Strategist: one-page strategy. Audience, one punch (5 words), proof, CTA, enemy.
3. Creative Director: 3 concepts, pick 1, kill 2. Name the meme frame.
4. Copywriter: 5 hooks, timed script (about 35 words), captions, social copy.
5. Visual Designer: look sheet + 3 styleframes. Palette 3 colours, type 2 faces.
6. Video Director: shot list, 5–8 shots. Product appears once, clearly, 2–3 seconds.
7. Animator: pick ONE motion style from `prompts/mg-styles.md`. 3-second hook test first.
8. Editor: cut, captions, sound -14 LUFS, export 9:16 + 1:1 + 16:9, thumbnail.
9. QA: claims, consent, licences, platform rules. Sign-off in writing.
10. Ship: upload masters + captions + thumbnail + delivery note.

## Deliverables
- Master video 9:16, plus 1:1 and 16:9 cuts
- Captions file (.srt), thumbnail (.jpg)
- Storyboard, shot list, prompts used, render steps, licence / consent notes
- Location: `outputs/<slug>/`

## QA gates
- Gate 1 (after step 4): script is timed, hook is in second 1–2, CTA is last 3 seconds only.
- Gate 2 (after step 7): 3-second hook test passes on a phone, sound-off.
- Gate 3 (after step 9): QA sign-off is "pass". No ship without it.

## Quality bar
- Hook in 1–2 seconds. One punch. Rewatchable.
- No hard sell before 80%. CTA in last 3 seconds.
- Captions on. Safe zones respected. Sound-off works.

## If it fails
- Hook fails: rewrite the first 2 seconds, not the whole ad.
- Drop-off at second 6: cut the setup, go to the twist faster.
- CTA unclear: make it one action, with where and by when.

## v2 render gate (code-rendered ads)

- Treatment first — before opening any demo or example. Run the "not the
  demo again" check: at least 4 of 6 must differ from the demo (structure,
  opening, signature shot, camera path, score shape, ending).
- Fonts first: download OFL fonts before rendering; vendor GSAP locally
  (`assets/gsap.min.js`); never rely on a CDN at render time.
- Render loop: `npx hyperframes lint` → `npx hyperframes check --json` →
  `npx hyperframes snapshot` (look at the frames) → `npx hyperframes render`.
- Render under the workspace with `TMPDIR` set there — /tmp is a 512 MB tmpfs.
- Vertical numbers: top 168px clear, text band 168–1330px, min 28px type,
  about 5 words per line, frame 0 is the thumbnail.
- Review loop: contact sheets, 0.2s strips, full-speed watch, one fix round,
  then a second-AI jury scored on a rubric (aim 9/10, fix the lowest first).
- Realistic footage, if any: client-supplied or licensed stock, composited in
  HyperFrames/Remotion, or an optional paid cloud video API. No local GPU model.
