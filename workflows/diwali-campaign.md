# Workflow: Diwali Campaign

## Goal
A Diwali campaign: one hero 30s film + two 15s reels + social cutdowns, all from one idea, one ritual, one offer.

## Time estimate
- Strategy + concepts: 2 hours
- Scripts: 2 hours
- Styleframes + shot list: 2 hours
- Shoot / generate: 1–2 days
- Edit + export + QA: 1 day
- Total: 3–5 days. Start 6 weeks before Diwali. Do not launch after Diwali.

## Agents involved
Strategist → Creative Director → Copywriter → Visual Designer → Video Director → Animator → Editor → QA / Brand Safety

## Skills to load
- ad-strategy, ad-creative-director, ad-copywriter-gen-z
- ad-visual-designer, ad-video-director, ad-animation-motion
- ad-diwali-festive, ad-social-formats, ad-brand-safety

## Steps
1. Scaffold the brief with the festival: `python3 scripts/new_ad.py --brand X --product Y --format reel15 --festival Diwali`
   Fill offer, dates, store, hallmark / proof. No blanks.
2. Read `docs/DIWALI_PLAYBOOK.md`. Pick ONE festive pattern: homecoming, gifting as peace,
   local shop, light in a dark moment, family argument resolved.
3. Strategist: audience (family, Tier-2/3 clarity), one punch, proof, CTA, enemy.
4. Creative Director: 3 concepts, pick 1. Name the ritual: what is actually happening?
5. Copywriter: hero 30s script + two 15s reel scripts from the same idea. Hinglish, natural.
   Captions for every line. Offer with a real end date in the CTA.
6. Visual Designer: Diwali look — maroon / gold / cream, warm diya light, family framing.
7. Video Director: shot list for hero + reels. Product appears once per film, clearly.
8. Animator: one motion style for the whole campaign. Consistent type and CTA.
9. Editor: cut hero + reels + 1:1 / 16:9 versions, captions, thumbnails, sound.
10. QA: claims, hallmark / BIS, offer dates, festive sensitivity, consent, licences.
11. Ship: hero + reels + cutdowns + delivery note, with launch dates.

## Deliverables
- Hero 30s film, two 15s reels, social cutdowns (9:16, 1:1, 16:9)
- Captions, thumbnails, storyboard, shot list, prompts, licences
- Launch calendar: festival date, launch date, shoot date
- Location: `outputs/<slug>/`

## QA gates
- Gate 1: offer is true, dated, and in the brief. No fake urgency.
- Gate 2: hook test passes for hero and for each reel, on a phone, sound-off.
- Gate 3: QA sign-off is "pass", including festive sensitivity.

## Quality bar
- A Tier-2 family sees themselves in it, not a metro stereotype.
- The ritual is the story. The product is the guest, not the host.
- The ad works without fireworks. Light, warmth and people carry it.

## If it fails
- Too much spectacle, no story: cut the fireworks, keep the family moment.
- Offer unclear: put the price and end date on screen, once, clearly.
- Late launch: a Diwali ad after Diwali is a miss. Move the launch, do not rush the shoot.

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
