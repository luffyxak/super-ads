# Workflow: Product Launch

## Goal
Launch a product in 10 days: teaser, reveal, UGC — three different ads, one punch.

## Time estimate
- Teaser: 2 hours
- Reveal 15s: 4–5 hours
- UGC briefs: 1 hour
- Total: 1–2 days for assets, 10 days for the launch arc.

## Agents involved
Strategist → Creative Director → Copywriter → Visual Designer → Video Director → Animator → Editor → QA / Brand Safety

## Skills to load
- ad-strategy, ad-creative-director, ad-copywriter-gen-z
- ad-visual-designer, ad-video-director, ad-animation-motion
- ad-social-formats, ad-brand-safety, ad-performance-analyst (after launch)

## Steps
1. Scaffold: `python3 scripts/new_ad.py --brand X --product Y --format launch10 --festival none`
2. Strategist: one punch (5 words), proof, price, launch date, CTA.
3. Creative Director: teaser idea (no product), reveal idea (product lands at second 10), UGC angles.
4. Copywriter: teaser 6s script, reveal 15s script, UGC briefs for 5 creators (different angles).
5. Visual Designer: launch look — one hero colour, product centre, clean.
6. Video Director / Animator: teaser, reveal, UGC guidance. Product appears once, clearly.
7. Editor: cut teaser + reveal + UGC guidance, captions, thumbnails, exports.
8. QA: price, claims, consent, licences. Sign-off.
9. Launch: Day -3 teaser, Day 0 reveal, Day +2 UGC, Day +7 iteration from performance data.
10. Performance Analyst: after 3–7 days, what worked, what to iterate, version 2.

## Deliverables
- Teaser 6s, reveal 15s, UGC briefs (5 angles)
- Masters 9:16 + 1:1 + 16:9, captions, thumbnails
- Launch calendar, prompts, licences
- Location: `outputs/<slug>/`

## QA gates
- Gate 1: price is true, dated, and in the brief.
- Gate 2: hook test passes for teaser and reveal.
- Gate 3: QA sign-off is "pass" before Day -3.

## Quality bar
- Teaser, reveal and UGC are different, not the same ad cut three ways.
- Product appears once, clearly, in use.
- Price appears once, big, clear, for 2 seconds, at the payoff.

## If it fails
- Teaser gives away the product: cut the product, keep the tension.
- Reveal is slow: product lands at second 10, not second 14.
- UGC all sounds the same: give each creator a different angle, not the same script.

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
