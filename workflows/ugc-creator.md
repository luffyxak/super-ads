# Workflow: UGC Creator

## Goal
Five creator ads that feel like people, not ads — same punch, five different angles.

## Time estimate
- Briefs: 1 hour
- Creator production: 2–3 days (creators shoot)
- Edit + QA: 1 day
- Total: 3–4 days.

## Agents involved
Strategist → Creative Director → Copywriter → Editor → QA / Brand Safety
(Creators are the performers. Do not direct them like actors in a TVC.)

## Skills to load
- ad-strategy, ad-copywriter-gen-z, ad-social-formats, ad-brand-safety
- ad-performance-analyst (after launch)

## Steps
1. Scaffold: `python3 scripts/new_ad.py --brand X --product Y --format reel15 --festival none`
2. Strategist: one punch, proof, CTA. One punch for all five creators.
3. Creative Director: five angles, one per creator: demo, reaction, comparison,
   day-in-life, joke. No two creators get the same angle.
4. Copywriter: one-page brief per creator: angle, hook, 3 talking points, what NOT to say,
   CTA line. No full script. Creators write in their own voice.
5. Creators shoot on their phones, in their homes, in natural light. No studio.
6. Editor: light touch only. Captions, safe zones, sound, export 9:16 + 1:1.
   Do not over-edit UGC into a TVC. Keep the imperfections that make it real.
7. QA: claims, consent, creator contract, disclosure (#ad / paid partnership), licences.
8. Ship: five masters + captions + delivery notes. Launch one per day, learn, iterate.

## Deliverables
- Five UGC masters (9:16, plus 1:1)
- Captions, thumbnails, creator briefs, contracts / disclosure notes
- Performance plan: what to measure, what to iterate
- Location: `outputs/<slug>/`

## QA gates
- Gate 1: each brief has a different angle, a hook, and a CTA — no full script.
- Gate 2: disclosure is correct: #ad / paid partnership, as the platform requires.
- Gate 3: QA sign-off is "pass", including creator consent.

## Quality bar
- Each ad sounds like its creator, not like the brand.
- The product is shown in use, not on a pedestal.
- Captions on. Sound-off works. Safe zones respected.

## If it fails
- All five sound the same: rewrite the briefs, give different angles.
- A creator reads a brand script: stop, let them rewrite it in their voice.
- Disclosure missing: fix it before upload. Do not ship without it.

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
