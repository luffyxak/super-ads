# Workflow: 30s TVC

## Goal
One 30-second TVC / long social film that tells a small story, lands one punch, and earns its 30 seconds.

## Time estimate
- Strategy + concepts: 1 hour
- Script + captions: 1 hour
- Styleframes + shot list: 1 hour
- Shoot / generate + motion: 4–6 hours
- Edit + export + QA: 2 hours
- Total: 1–2 days for a first version.

## Agents involved
Strategist → Creative Director → Copywriter → Visual Designer → Video Director → Animator → Editor → QA / Brand Safety

## Skills to load
- ad-strategy, ad-creative-director, ad-copywriter-gen-z
- ad-visual-designer, ad-video-director, ad-animation-motion, ad-realistic-video
- ad-social-formats, ad-brand-safety

## Steps
1. Scaffold the brief: `python3 scripts/new_ad.py --brand X --product Y --format tvc30 --festival none`
2. Strategist: one-page strategy. One punch, proof, CTA, enemy.
3. Creative Director: 3 concepts, pick 1, kill 2. Name the meme frame and the emotional beat.
4. Copywriter: 5 hooks, timed script (about 70 words), captions, social copy.
   Beats: 0–2 hook, 2–8 setup, 8–20 twist/demo, 20–27 payoff, 27–30 CTA.
5. Visual Designer: look sheet + 3 styleframes. Light, palette, type.
6. Video Director: shot list, 10–14 shots. Performance notes per shot. Sound plan.
7. Animator / Realistic Video: motion style + realistic takes. 3 takes per shot, pick the best.
8. Editor: cut, captions, sound mix, export 9:16 + 1:1 + 16:9, thumbnail.
9. QA: claims, consent, licences, platform rules, accessibility. Sign-off in writing.
10. Ship: masters + captions + thumbnail + delivery note.

## Deliverables
- Master video 9:16, plus 1:1 and 16:9 cuts
- Captions file, thumbnail, storyboard, shot list, prompts, render steps, licences
- Location: `outputs/<slug>/`

## QA gates
- Gate 1 (after step 4): script is timed at 30s, hook in second 1–2.
- Gate 2 (after step 7): hook test + one full beat test pass on a phone.
- Gate 3 (after step 9): QA sign-off is "pass".

## Quality bar
- The story earns 30 seconds. If it could be 15 seconds, cut it to 15.
- One punch. One emotional beat. One CTA.
- Performance is specific. Sound is planned, not added at the end.

## If it fails
- Setup too long: cut the setup to 6 seconds, go to the twist faster.
- Payoff weak: the payoff must earn the CTA. Rewrite the payoff, not the hook.
- Over 30 seconds: cut 20% of the words, then cut again.

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
