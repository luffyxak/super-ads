# Trigger eval — should-trigger vs should-not-trigger queries

Use this set to test whether a skill's description triggers when it should
and stays quiet when it should not. 20 queries per skill: 10 should-trigger
(realistic, detailed), 10 should-not-trigger (near-misses — not obviously
irrelevant negatives). Run each query 3 times, 60% train / 40% held-out,
and take the best description by *test* score, not train score.

## ad-strategy (10 should / 10 should-not)

Should trigger:
1. "Starting a new ad for our Diwali gold offer — help me position it."
2. "The brief is vague and the product has no clear reason to care."
3. "Two concepts both look good — which one do we pick?"
4. "What is the one thing viewers should remember from this ad?"
5. "Our fintech app has no clear punch. Fix the positioning."
6. "Write a one-page strategy: audience, punch, proof, CTA."
7. "We are launching a mango drink — who is it for and what is the enemy?"
8. "The client wants three messages in one ad. Help me cut it to one."
9. "Position this for Tier-2 India, Hinglish, family buyers."
10. "Give me the strategy before anyone writes a joke."

Should NOT trigger:
1. "Write me 5 hooks for this concept." (copywriter)
2. "Animate the hook text popping in on the beat." (animation-motion)
3. "Is this claim safe to ship?" (brand-safety)
4. "Make a thumbnail for this reel." (social-formats)
5. "Render the ad in HyperFrames." (animation-motion)
6. "What is the drop-off second for this ad?" (performance-analyst)
7. "Write the shot list for this script." (video-director)
8. "Pick a palette for this Diwali ad." (visual-designer)
9. "Check the licence on this music track." (brand-safety)
10. "Give me 3 concepts for this strategy." (creative-director — strategy
    already exists; this is concept work, not positioning)

## ad-animation-motion (10 should / 10 should-not)

Should trigger:
1. "Animate this ad — kinetic type, words pop on the beat."
2. "Render the ad in HyperFrames, 9:16, 30 fps."
3. "Make a template so we can swap the price and city per version."
4. "The hook text is not readable in 1 second — fix the timing."
5. "Run the lint-check-snapshot-render loop on this project."
6. "The render failed with sub_timeline_script_failure — what do I do?"
7. "Set up the motion map: element, enter, hold, exit per beat."
8. "Motion test: 3 seconds, hook only."
9. "Which style from mg-styles.md fits this ad?"
10. "Vendor GSAP locally — the CDN render keeps failing."

Should NOT trigger:
1. "Generate a realistic street scene with AI video." (realistic-video)
2. "Write the script for this concept." (copywriter)
3. "Is this celebrity likeness safe to use?" (brand-safety)
4. "Position this ad for Diwali buyers." (strategy)
5. "Export the 1:1 cut." (social-formats)
6. "Give me 3 concepts." (creative-director)
7. "What font should the hook use?" (visual-designer — look, not motion)
8. "Analyse why people dropped off at second 12." (performance-analyst)
9. "Write the shot list." (video-director)
10. "Check the music licence." (brand-safety)

## ad-realistic-video (10 should / 10 should-not)

Should trigger:
1. "I need a realistic street scene and cannot shoot it."
2. "What realistic footage can we use on a CPU-only machine?"
3. "Can we use stock footage for this Diwali home scene?"
4. "What are the paid cloud video API options for one realistic shot?"
5. "Composite this supplied product footage into the HyperFrames ad."
6. "The client sent us their own footage — how do we use it in the ad?"
7. "We need many variations of the same realistic scene."
8. "Check this realistic shot frame by frame for hands and text."
9. "What are the limits of using stock footage in a paid ad?"
10. "License check: is this Pexels clip cleared for commercial use?"

Should NOT trigger:
1. "Animate the hook text popping in." (animation-motion)
2. "Render the motion-graphics template." (animation-motion)
3. "Write a kinetic-type ad." (animation-motion)
4. "Give me a motion style from mg-styles.md." (animation-motion)
5. "Write the script." (copywriter)
6. "Position the ad." (strategy)
7. "Make the thumbnail." (social-formats)
8. "Is this claim safe?" (brand-safety)
9. "Analyse the drop-off." (performance-analyst)
10. "Run the HyperFrames render loop." (animation-motion)

## Grading notes

- A trigger is correct only if the skill loads for the query's job. Loading
  the wrong skill is a miss, even if the output looks fine.
- Near-misses matter most: "write the shot list" must not trigger the
  animation skill, and "render the ad" must not trigger the realistic-video
  skill. If a description is too broad, narrow it with a DO-NOT boundary.
- Record per-query results (query, expected skill, loaded skill, pass/fail)
  in `evals/runs/trigger-<skill>-<date>.md` before changing a description.
