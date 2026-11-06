# Studio harness

## Repository and execution map

The creative system is authored in `workflows/`, `agents/`, and `skills/`. The eight role files and 11 skills remain canonical. Claude discovers the root directories. Codex scans `.agents/skills`; its relative symlinks resolve to the same skill folders. The Studio reads the current role and one designated reference per routed skill. [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

`studio/contracts.py` owns IDs, stage order, asset roles, timelines, and hard gates. `studio/store.py` owns SQLite state, transactions, revisions, redacted events, and attempts. `studio/server.py` and `python3 -m studio` share that store. Browser assets live in `studio/web`. `studio/render.py` is the trusted HyperFrames scene implementation. `studio/reports.py` assembles documents from the same snapshot. `tests/` and `evals/` exercise the product and harness respectively.

The design uses small project-specific instructions, bounded packets, and repeatable feedback. Stage outputs become checkpoints. A rubric and media inspection are separate from assertion-based evaluation. [OpenAI harness engineering](https://openai.com/index/harness-engineering/) · [Anthropic harness design](https://www.anthropic.com/research/harness-design-long-running-apps) · [Google behavioral evaluation](https://developers.googleblog.com/en/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/) · [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) · [OpenAI harness-aware evals](https://developers.openai.com/cookbook/examples/partners/harness_aware_plugin_evals/harness_aware_plugin_evals)

## Workflow resolution

| Workflow | Films and branches |
|---|---|
| 15s reel | One 15-second reel |
| 30s TVC | One 30-second hero |
| Diwali | 30-second hero, two 15-second reels, launch calendar and dated offer |
| Product launch | 15-second reveal, 6-second teaser, creator guidance and launch calendar in the handoffs |
| Creator UGC | Five editable 15-second creator timelines. Human capture follows creator briefs, and captioning/editing follows capture |
| Big event | 30-second hero, 15-second cutdown, 6-second teaser, launch calendar |

Studio ratios follow the root delivery policy and include landscape for UGC. Drafts and authored standalone workflows can be used for creator vertical/square review. The scaffold keeps `launch10` as a legacy entry point. The executable launch profile follows the authored 6-second teaser and 15-second reveal. The authored copywriting task can brainstorm five hooks. Studio stores up to three editable variants, with one declared variable. The fixed 15-second UGC starting profile is a Studio default. Direct all actual publishing outside Studio.

The main route is strategist, creative director, copywriter, visual designer, video director, animator, editor, QA. Festive context attaches to strategy when the workflow or festival calls for it. Realistic footage attaches to motion when selected. UGC has a creator capture checkpoint and skips studio shot direction and animation. Actual metrics append an operator analysis handoff after client approval. Measurement hypotheses live in the brief and remain distinct from results.

The app checks brief inputs, risk flags, offer dates, caption bounds, shot duration, opening/CTA beats, references, consent fields, rights, and render integrity. QA reads the creative content and supporting proof. Presence checks cannot establish whether a document is genuine or whether a text promise is true. Capture disclosure, rights scope, headline and CTA readability, sound-off comprehension, and craft remain review tasks. Local review and approval identities are attestations on a single-operator machine.

## State, attempts, and data

Every successful mutation is a SQLite revision with optimistic revision checking inside a write transaction. The app retains prior snapshots and addresses media by its validated identity. A changed brief invalidates from strategy, and a shot retake invalidates from shot direction or creator capture. The rendering worker reserves a single attempt before invoking trusted tools, publishes completed files in an attempt-specific directory, and commits their hashes. Cancellation cleans incomplete output. On restart, a dead worker returns the run to its last durable handoff. An interrupted provider attempt is ambiguous and requires explicit operator resolution.

The independent reviewer records timecoded notes and six rubric scores. Human approval binds the current picture input and exact render hash set. Edits and review changes clear the approval. The bundle rehashes the source files. The fictional example can record a demo approval test, while its release gate remains closed. Report creation and bundle creation are separate actions.

The server binds IPv4 loopback and rejects other hosts and browser origins. It never serves a filesystem path from a request. It accepts JSON actions and known media types within explicit size bounds. Media bytes are signature-checked, probed, and decoded before import. Trusted templates escape project text. Media and workspaces reject symlinks. Operators should keep the data directory private. SQLite history contains creative material and is subject to the same local handling as assets. Traces omit model text, credentials, and tool logs.

## Agent boundary

The keyless default uses manual stage output or explicitly labeled Quiet Hours fixtures. The opt-in CLI adapter uses OpenAI Responses with strict JSON Schema and no tools. Codex CLI is suitable for operator-driven repo work. The production adapter uses a tool-free request so briefs and upstream artifacts cannot cause a shell command, filesystem write, or browser operation. [Codex integration options](https://developers.openai.com/blog/codex-as-a-platform) · [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

Inspect the authorized brief and accepted upstream handoffs before invoking `python3 -m studio agent PROJECT --allow-provider` with a separately configured `OPENAI_API_KEY`. The adapter sends text from these inputs to the official API with `store: false`; consult account retention settings for your project. It sends no media bytes or consent files. The operator authorizes each invocation. There is a 50 KiB input ceiling, 1,800-token response budget, 30-second transport timeout and 12-call project ceiling. A rejected 429 can retry twice. Ambiguous responses are surfaced without automatic repeat. Account billing determines monetary cost. Keep provider project budgets configured independently. Live provider grading requires separate authorization.

## Production and verification

- [Production patterns](STORYFORGE_PRODUCTION.md) covers continuity, retakes, manual external clips, and sound.
- [Source audit](SOURCE_AUDIT.md) distinguishes legacy evidence, bundled material, and authored sources.
- [Release evidence](PROGRESS.md) records tested commands and remaining boundaries.
- Install the dependencies and run `python3 scripts/verify_studio.py`. Run `python3 scripts/validate_repo.py` before every commit and delivery. Keep the CI runner keyless.
