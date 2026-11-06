> v2 note: this example follows the v2 rules — treatment first, one motion
> style, the HyperFrames lint → check → snapshot → render loop, vertical
> numbers (top 168px clear, text band 168–1330px), -14 LUFS measured, and a
> second-AI jury before QA sign-off. Realistic shots use supplied or licensed
> stock footage composited in HyperFrames/Remotion, or an optional paid cloud
> video API — no local GPU model is part of this repo.

# Example: Fintech — 30s Moonshot-Style

## Brief
- Brand: PayQuick (fictional)
- Product: UPI in 2 taps
- Audience: 22-year-olds who hate bank forms, metro + Tier-2, Hinglish
- Problem: Bank apps ask for 10 steps for a simple payment.
- One punch: "UPI in 2 taps." (4 words)
- Proof: Timed screen recording in the ad — 2 taps, done in 4 seconds.
- CTA: "Download PayQuick — UPI in 2 taps." Last 3 seconds.

## Moonshot pattern used
- Celebrity subversion, not endorsement: a serious actor, known for calm roles, is angry.
- Medium is the joke: the form itself is the villain. The phone is the hero.
- Challenger energy: punch up at slow banks, not down at users.
- Deadpan delivery: the angrier he is, the funnier it is. Then he calms down in 2 taps.

## 3 concepts
- A. Angry actor vs form: A serious actor fills a 10-page form, gets angrier, then taps twice and calms down.
- B. Bank as a maze: A user walks through a maze of counters, then taps twice and exits.
- C. Grandma vs app: A grandmother pays faster than her grandson. Funny, but the product gets lost.
- Picked: A. Killed: B — needs a set, slow. C — sweet but the punch is not the product.

## Chosen script — 30s, about 70 words
| Time | Visual | Audio | Caption |
|---|---|---|---|
| 0–2s | Close-up, serious actor stares at a paper form, deadpan | "Ye form hai, ya exam?" | Ye form hai, ya exam? |
| 2–8s | He flips pages, each page longer, angrier | Paper rustle, no music | Page 1… page 10… |
| 8–20s | Phone on table. He taps twice. Success tick. He relaxes, smiles | Tick sound, music in | 2 taps. Ho gaya. |
| 20–27s | He looks at camera, calm | "UPI in 2 taps. Bas." | UPI in 2 taps. Bas. |
| 27–30s | Product + CTA text on screen | "Download PayQuick" | Download PayQuick |

## Storyboard
Shots: 1 close-up form, 2 pages flipping, 3 phone 2 taps, 4 actor calm, 5 CTA.
Product appears once, clearly, in use, for 2–3 seconds. The demo is timed on screen.

## Video prompts
- Shot 1: "9:16, close-up, serious man stares at a paper form, deadpan, hard daylight, static camera, 24fps."
- Shot 3: "9:16, over-shoulder, phone screen shows payment app, finger taps twice, green tick, bright daylight, 24fps."
- Negative: no shouting, no warped phone screen, no extra fingers, no morphing.

## Render steps
1. Motion style: Kinetic Pop from `prompts/mg-styles.md`. 30fps, 1080x1920.
2. Hook test: 3 seconds, shot 1 only. Pass if the hook line lands deadpan.
3. Full render: HyperFrames for the type; the performance uses a consenting actor on set, or supplied/licensed footage composited in HyperFrames. Render loop: lint → check --json → snapshot → render. Sound -14 LUFS measured.
4. Captions: burned-in + SRT. Sound -14 LUFS.
5. QA: actor consent and contract, "2 taps" proof (timed recording), no "best" claim without proof.

## Captions
- "Ye form hai, ya exam?"
- "Page 1… page 10…"
- "2 taps. Ho gaya."
- "UPI in 2 taps. Bas."
- "Download PayQuick"

## Why it works
- The star is the joke, not the pitch. The anger is the hook.
- The demo is the proof. Two taps, timed, on screen.
- No hard sell before 80%. The CTA is the last 3 seconds, once.
