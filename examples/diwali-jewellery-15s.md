> v2 note: this example follows the v2 rules — treatment first, one motion
> style, the HyperFrames lint → check → snapshot → render loop, vertical
> numbers (top 168px clear, text band 168–1330px), -14 LUFS measured, and a
> second-AI jury before QA sign-off. Realistic shots use supplied or licensed
> stock footage composited in HyperFrames/Remotion, or an optional paid cloud
> video API — no local GPU model is part of this repo.

# Example: Diwali Jewellery — 15s Reel

## Brief
- Brand: Test Jewellers, Jaipur
- Product: Diwali gold bangles, BIS hallmarked
- Offer: Making charges 12% off till 8 Nov, Jaipur store + online
- Audience: Families buying first gold for Diwali in Jaipur, Tier-2 clarity, Hinglish
- Problem: Gold feels expensive and confusing. Families delay the purchase.
- One punch: "Gold that comes home for Diwali." (5 words)
- Proof: BIS hallmark on every piece, offer sheet dated 5 Nov 2026
- CTA: "Visit Test Jewellers, Jaipur — offer till 8 Nov." Last 3 seconds.

## 3 concepts
- A. Homecoming: A son returns, the house lights up, gold is the welcome.
  Meme frame: the diya reflected in the bangle.
- B. Neighbours argue: Parking, walls, pets — a box of sweets ends it, gold is the gift inside.
  Meme frame: two neighbours smiling over the box.
- C. Nani approves: A grandmother inspects the bangles, nods once. That nod is the ad.
  Meme frame: nani's nod, close-up.
- Picked: C — Nani approves. It is warm, specific, and rewatchable.
  Killed: A — beautiful but seen before. B — funny but the gold gets lost in the argument.

## Chosen script — 15s, about 35 words
| Time | Visual | Audio | Caption |
|---|---|---|---|
| 0–2s | Close-up, nani looks at camera, deadpan | "Ye sone ka hai?" (Is this gold?) | Ye sone ka hai? |
| 2–6s | Hands open a maroon box, gold bangles catch diya light | Soft music, diya crackle | Diya light, gold shine |
| 6–12s | Nani lifts a bangle, inspects it, smiles, nods once | Music swells slightly | Nani ne haan keh diya |
| 12–15s | Bangles on a wrist, CTA text on screen | "Test Jewellers, Jaipur — 12% off making charges till 8 Nov" | Visit Test Jewellers — till 8 Nov |

## Storyboard table
See `templates/storyboard-template.md`. Shots: 1 close-up nani, 2 box open, 3 bangle inspect,
4 wrist close-up, 5 CTA. Product appears once, clearly, in use, for 2–3 seconds.

## Video prompts
- Shot 1: "9:16, close-up, elderly Indian woman looks at camera, deadpan, warm diya light, 24fps."
- Shot 2: "9:16, extreme close-up, hands lift gold bangles from a maroon velvet box, gold catches diya light, shallow depth of field, 24fps."
- Shot 3: "9:16, close-up, elderly woman smiles and nods once, warm light, 24fps."
- Shot 4: "9:16, close-up, gold bangles on a wrist, diya light, 24fps."
- Negative for all: no extra fingers, no plastic-looking gold, no warped text, no morphing.

## Render steps
1. Motion style: Smooth Premium from `prompts/mg-styles.md`. 24fps, 1080x1920.
2. Hook test: 3 seconds, shot 1 only, on a phone, sound-off. Pass if the hook line is readable in 1 second.
3. Full render: HyperFrames (primary — see examples/hyperframes-diwali-8s/ for the proven pattern) or Remotion. Render loop: lint → check --json → snapshot (look at the frames) → render. Export 9:16 + 1:1 + 16:9.
4. Captions: burned-in + SRT. Sound -14 LUFS.
5. QA: hallmark proof, offer dates, consent for the actor, music licence. Sign-off in writing.

## Captions
- "Ye sone ka hai?"
- "Diya light, gold shine"
- "Nani ne haan keh diya"
- "Visit Test Jewellers — till 8 Nov"

## Why it works
- Hook in 2 seconds, one punch, one nod as the payoff.
- The product is the guest, not the host. The family is the story.
- Tier-2 clarity: price, hallmark, date, store — all in the last 3 seconds, once, clearly.
