# Workflow: Super-Bowl-Style

## Goal
One big-event ad (Super Bowl, IPL final, World Cup) that is worth the big-event price —
a story, a star used right, and a moment people talk about the next day.

## Time estimate
- Strategy + concepts: 1 day
- Script + casting: 2–3 days
- Shoot / generate: 3–5 days
- Edit + QA: 2 days
- Total: 1–2 weeks. Start early. Big events do not forgive a rush.

## Agents involved
Strategist → Creative Director → Copywriter → Visual Designer → Video Director → Animator → Editor → QA / Brand Safety

## Skills to load
- ad-strategy, ad-creative-director, ad-copywriter-gen-z
- ad-visual-designer, ad-video-director, ad-animation-motion, ad-realistic-video
- ad-social-formats, ad-brand-safety

## Steps
1. Scaffold: `python3 scripts/new_ad.py --brand X --product Y --format tvc30 --festival none`
2. Strategist: one punch, proof, CTA, enemy. Why does this brand deserve a big-event slot?
3. Creative Director: 3 concepts, pick 1. Celebrity subversion, not endorsement.
   The star is the joke, not the pitch. Medium is the joke.
4. Copywriter: 30s script, 5 hooks, captions, social copy. The ad must work as a 30s film
   AND as a 15s cutdown AND as a 6s teaser.
5. Visual Designer: big-event look — bold, simple, readable on a TV and on a phone.
6. Video Director: shot list, performance, sound. Plan the moment people will screenshot.
7. Animator: motion for cutdowns and teasers. One style for the whole campaign.
8. Editor: hero 30s, cutdown 15s, teaser 6s, exports 9:16 + 1:1 + 16:9, thumbnails.
9. QA: claims, celebrity consent and contract, licences, platform rules. Sign-off.
10. Ship: hero + cutdowns + teasers + delivery note, with a launch plan for the event day.

## Deliverables
- Hero 30s, cutdown 15s, teaser 6s
- Masters 9:16 + 1:1 + 16:9, captions, thumbnails
- Storyboard, shot list, prompts, licences, consent proofs
- Location: `outputs/<slug>/`

## QA gates
- Gate 1: celebrity is subverted, not just endorsing. Contract and consent in hand.
- Gate 2: hook test passes for hero, cutdown and teaser.
- Gate 3: QA sign-off is "pass". No big-event spend without it.

## Quality bar
- The ad is talked about the next day for the idea, not only for the star.
- It works as a 30s film, a 15s cutdown, and a 6s teaser.
- One punch. One meme frame. One CTA.

## If it fails
- The star is bigger than the idea: rewrite so the idea carries the ad.
- The ad only works at 30s: cut a 15s version that stands alone.
- The joke needs the event to make sense: make it work without the event too.

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
