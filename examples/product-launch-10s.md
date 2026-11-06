> v2 note: this example follows the v2 rules — treatment first, one motion
> style, the HyperFrames lint → check → snapshot → render loop, vertical
> numbers (top 168px clear, text band 168–1330px), -14 LUFS measured, and a
> second-AI jury before QA sign-off. Realistic shots use supplied or licensed
> stock footage composited in HyperFrames/Remotion, or an optional paid cloud
> video API — no local GPU model is part of this repo.

# Example: Product Launch — 10s

## Brief
- Brand: GlowSip (fictional)
- Product: Mango sparkling water, 0g added sugar
- Audience: Gym-goers who hate sugary drinks, 20–30, metro
- Problem: Mango drinks are sweet, then a sugar crash.
- One punch: "Mango, no sugar crash." (4 words)
- Proof: 0g added sugar on the label, shown close-up.
- CTA: "Try GlowSip — in stores now." Last 3 seconds.

## Concept
- The product is missing for 7 seconds. Everyone looks for it.
- Twist: it was in the hero's hand the whole time.
- Payoff: she opens it, drinks, smiles. Label close-up: 0g added sugar.

## Script — 10s, about 22 words
| Time | Visual | Audio | Caption |
|---|---|---|---|
| 0–2s | Close-up, hero looks around, confused | "Where is it?" | Where is it? |
| 2–7s | Friends look under a bench, in a bag, behind a bottle | Music, fast | Still looking… |
| 7–10s | She lifts her hand — the can was there. Opens it, drinks | Pop sound, music out | Mango, no sugar crash. Try GlowSip. |

## Storyboard
Shots: 1 close-up confused, 2 searching, 3 hand lift + can, 4 label close-up + CTA.
Product appears at second 7, clearly, in use, for 3 seconds.

## Video prompts
- Shot 1: "9:16, close-up, young woman looks around, confused, gym, daylight, 24fps."
- Shot 3: "9:16, close-up, hand lifts a mango sparkling water can, condensation, bright light, 24fps."
- Shot 4: "9:16, extreme close-up, can label shows 0g added sugar, sharp, 24fps."
- Negative: no warped label, no extra cans, no text errors.

## Render steps
1. Motion style: Zoom Punch from `prompts/mg-styles.md`. 30fps, 1080x1920.
2. Hook test: 3 seconds, shot 1 only.
3. Full render: 10 seconds, export 9:16 + 1:1 + 16:9.
4. Captions: burned-in + SRT. Sound -14 LUFS.
5. QA: label claim "0g added sugar" checked against the real label, consent, licences.

## Captions
- "Where is it?"
- "Still looking…"
- "Mango, no sugar crash. Try GlowSip."

## Why it works
- 10 seconds, one joke, one reveal. No explanation.
- The product is the punchline, not a pack shot.
- The claim is on the label, in the frame, provable.
