---
description: Review a finished ad against the QA checklist — claims, consent, licences, render checks — and give a written sign-off
allowed-tools: Read, Glob, Grep, Bash(ffprobe:*)
---

# /review-ad

Review a finished ad and give a written sign-off. Arguments: `$ARGUMENTS` —
the delivery folder (for example `outputs/<slug>`).

Example: `/review-ad outputs/test-jewellers-diwali-gold-bangles-diwali`

## Steps

1. Load `skills/ad-brand-safety` and `agents/qa-brand-safety.md`. This is the
   final gate — do not skip it, and do not sign off an ad you have not watched.
2. Watch all three cuts (9:16, 1:1, 16:9) if they exist, and read the captions
   file. Check the safe zones (top 168px clear, text band 168–1330px),
   the hook in the first 2 seconds, sound-off readability, and the CTA in the
   last 3 seconds only.
3. List every claim (price, discount, "best", "first", "No.1", "free",
   "guaranteed") with proof and source. No proof, no claim — cut the line.
4. List every person with consent proof. No consent, no likeness.
5. Check licences for every asset (music, fonts, footage, stock) and keep the
   proof in the delivery folder. Check the render: `ffprobe` the MP4 for
   duration, resolution, and fps; check the sound is -14 LUFS.
6. Run the second-AI jury: score the ad 1–10 on hook, timing, type, motion,
   sound, brand, rewatchability. Aim for 9. Fix the lowest score first, and
   list the honest top-3 weaknesses.
7. Write the sign-off: pass, pass with fixes, or fail — with fixes listed by
   shot number. If "pass with fixes", hand back to the editor with the fix
   list. If "fail", hand back to the creative director with the reason.
   Never hand a failing ad to the client.
