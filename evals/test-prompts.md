# Test prompts — with-skill vs baseline

Run each prompt twice: once with the skill loaded, once without (baseline).
Grade with the assertions listed. Record results in `evals/runs/` and
aggregate into `benchmark.md`. No runs have been executed yet.

## 1. ad-strategy — "starting a new ad"

Prompt: "We are a Jaipur jewellery shop launching a Diwali gold bangles
offer: BIS hallmarked, making charges 20% off till 8 Nov, in-store only.
Write the strategy. The audience is families buying their first gold for
Diwali. The punch must be 5 words max."

Assertions:
- [ ] Output has audience, problem, one punch (5 words max), proof + source,
      CTA (last 3 seconds), enemy, and 3 "will NOT say" lines.
- [ ] The punch is about the viewer, not the brand.
- [ ] The offer date and proof are carried through, not invented.
- [ ] No script, hooks, or shot list in the output (handoff, not scope creep).

## 2. ad-creative-director — "this idea is boring"

Prompt: "Strategy: audience — 22-year-olds who hate bank forms. Punch —
'UPI in 2 taps.' Proof — a live demo, timed on screen. Give me 3 concepts
and pick 1."

Assertions:
- [ ] Three concepts, different in kind (emotional, funny, subversive).
- [ ] Each concept names a meme frame.
- [ ] One picked with a reason, two killed with a reason each.
- [ ] The picked concept passes the Moonshot test (subversion, not endorsement).

## 3. ad-copywriter-gen-z — "write the script"

Prompt: "Concept: a serious man is angry at a paper bank form; he taps his
phone twice and relaxes. Write a 30-second script with 5 hooks, captions,
and social copy."

Assertions:
- [ ] Five hooks, 6 words or fewer each, in seconds 1–2.
- [ ] Script is timed by beats, about 70 words, CTA only in the last 3 seconds.
- [ ] Captions cover every line, 2 lines max, 32 characters per line.
- [ ] No corporate words (leverage, ecosystem, seamless, revolutionary).

## 4. ad-animation-motion — "animate this"

Prompt: "Animate this 15s Diwali reel for gold bangles in HyperFrames:
hook words pop on the beat, product lands at 10 seconds, CTA holds 3 seconds.
9:16, 30 fps."

Assertions:
- [ ] Output names ONE style from prompts/mg-styles.md, with a reason.
- [ ] Output gives a motion map (element, enter, hold, exit) per beat.
- [ ] Output states the render contract: clip rules, fromTo not from,
      paused timelines on window.__timelines, fonts first, TMPDIR under the
      workspace, lint → check → snapshot → render.
- [ ] Output does NOT say HyperFrames is Python and does NOT say pip install.

## 5. ad-realistic-video — "realistic video"

Prompt: "I need a realistic street scene at dusk for a 15s ad, no shoot
possible. What are my options on a CPU-only machine?"

Assertions:
- [ ] Output does NOT recommend a local GPU video model (no local model is
      named as runnable here).
- [ ] Output offers client-supplied or licensed stock footage composited in
      HyperFrames/Remotion, and optionally a paid cloud video API.
- [ ] Output states the machine limit honestly (no GPU here).
- [ ] Output includes the consent rule for real people.

## 6. ad-brand-safety — "can we ship"

Prompt: "Review this ad: 'No.1 gold shop in Jaipur, 50% off everything,
Diwali only!' A celebrity lookalike appears for 2 seconds. Can we ship?"

Assertions:
- [ ] "No.1" is flagged with no proof, no claim — cut the line.
- [ ] "50% off everything" is flagged (no real product at 50% off).
- [ ] The celebrity lookalike is flagged without consent proof.
- [ ] Sign-off is pass / pass with fixes / fail, with fixes by shot number.
