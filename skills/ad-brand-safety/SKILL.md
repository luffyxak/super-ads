---
name: ad-brand-safety
description: >-
  Check claims, consent, licences, and platform rules before an ad ships. Use as the final gate every time, and whenever a concept uses a real person, a claim, a price, a competitor, a child, or a religious moment. Trigger phrases: 'check this ad', 'is this claim safe', 'do we have consent', 'final gate', 'can we ship'. Delivers a written sign-off: pass, pass with fixes, or fail. Do NOT use to write the ad — this skill only judges it — and never sign off an ad you have not watched in full.
license: MIT
---
# Ad Brand Safety

## When to use
- As the final gate, every time. No ship without this skill.
- When an ad uses a real person, a celebrity, a child, a religious moment, or a competitor.
- When a claim, price, discount, or "best / No.1" line appears anywhere.

## Workflow
1. List every claim in the ad: price, discount, "best", "first", "No.1", "free", "guaranteed".
   For each claim, write the proof and the source. No proof, no claim. Cut the line.
2. List every person in the ad: actor, creator, celebrity, child, voice.
   For each person, write the consent proof: contract, release, date, scope.
   No consent proof, no likeness. Do not use a real person's face or voice without it.
3. Check deepfake / face-swap: this repo has no face-swap workflow. If a concept needs it, stop.
   Offer a fictional character or a consenting actor instead. Never generate a real person.
4. Check licences: music, fonts, footage, stock, AI model outputs. Write the licence
   and the file name for each asset. Keep proof in `outputs/<slug>/`.
5. Check platform rules: Meta, YouTube, TikTok — claims, before/after, financial products,
   health, alcohol, gambling, children's ads. If a rule is unclear, cut the risky line.
   Do not argue with the platform. The ad will be rejected and the account can be flagged.
6. Check accessibility: captions on, contrast, no flashing at 3 per second or more,
   no text that only appears for 0.5 seconds.
7. Check India-specific rules: ASCI guidelines, festive sensitivity, religious moments,
   price transparency, hallmark / BIS for gold, UPI / financial claims.
8. Sign off in writing: pass, pass with fixes, or fail. List fixes by shot number.
   Hand the sign-off to the editor. No sign-off, no ship.

## Output format
- Claims table: claim, proof, source, pass / fail
- People table: person, role, consent proof, scope, pass / fail
- Licences table: asset, licence, file name
- Platform check: Meta / YouTube / TikTok — pass / fail per rule
- Sign-off: pass / pass with fixes / fail + fixes by shot

## Quality bar
- Every claim has proof. Every person has consent. Every asset has a licence.
- A stranger could audit the ad from the delivery folder alone.
- The ad is safe to run in India, on Meta, YouTube and TikTok, without edits.

## Examples
- Gold: "BIS hallmarked, making charges 12% off till 8 Nov at Jaipur store" — proof is the store offer sheet.
- Fintech: "UPI in 2 taps" — proof is a timed screen recording in the ad.
- "No.1" — proof is a named source, date, and market. Otherwise cut it to "loved by" with no rank.

## Anti-patterns
- "Up to 50% off" with no real product at 50% off.
- A celebrity lookalike or voice clone without consent.
- A child in an ad without a guardian release and a clear role.
- "Best" with no source. Cut it.

## References
- `references/licence-checklist.md` — Licence checklist — claims, consent, asset licences, platform rules, India rules.
- Read only the reference file for the step you are on; do not load every reference at once.
