# Evals — how to test this repo's skills

Skills that have never been run are not production-ready. This folder holds
the test prompts, the trigger eval set, and the grading notes. Nothing here
is a claim about a run that did not happen — a benchmark is only written
after a run exists.

## The loop (from the Agent Skills skill-creator guide)

1. Write 2–3 realistic test prompts per skill or workflow (see
   `test-prompts.md`).
2. Run each prompt twice in parallel — once with the skill loaded, once
   without (baseline) — into `evals/runs/<skill>/iteration-N/eval-<name>/with_skill/`
   and `without_skill/`.
3. While the runs are in flight, draft objectively verifiable assertions
   (things that are true or false, not vibes).
4. Grade with a grader agent or a script into `grading.json` with fields
   `text`, `passed`, `evidence`.
5. Aggregate into `benchmark.md` (pass rate, time, tokens, mean ± stddev,
   delta with-skill vs baseline). Do an analyst pass for non-discriminating
   assertions and flaky evals. Improve the skill. Repeat.
6. Description optimisation: run the trigger eval set (`trigger-eval.md`,
   20 queries per skill — 10 should-trigger, 10 should-not-trigger, realistic
   and near-miss, not obviously irrelevant). Take the best description by
   *test* score, not train score (60% train / 40% held-out, each query 3×).

## What counts as a pass

- With-skill output follows the skill's output format exactly.
- With-skill output is better than baseline on the assertions, not just
  different. If the skill does not change the output, the skill is not
  triggering or not helping — fix the description first.
- No invented facts: prices, dates, claims, and licences in test outputs
  must be marked as placeholders, never presented as real.

## Keyless results

Run `python3 -m evals.run` from the repository root. The recorded run passed 39/39 cases: 22 skill packet routing positives and near-misses, six authored workflow runs, and 11 adversarial cases. The harness grades routing, durable handoffs, trace evidence, and structured artifacts. Tests use fixture handoffs and synthetic verification records where specified. No live model trials were run.

See the Quiet Hours evidence for real rendering and the separate creative rubric.
