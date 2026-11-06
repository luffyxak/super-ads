# Super Ads Studio

Read [README.md](README.md) and [CLAUDE.md](CLAUDE.md) before changing the repository. Read [the harness contract](docs/HARNESS.md) before changing state, providers, or release behavior. Resume from [the progress record](docs/PROGRESS.md).

- Use the one workflow selected from [workflows](workflows). Follow the authored role order and load only the current role, relevant skill, and reference. The executable registry lives in [studio/contracts.py](studio/contracts.py).
- Keep strategy, concept, copy, visuals, shot direction, motion, edit, and QA separate. Creator-shot UGC has an operator capture handoff. Observed analysis requires actual metrics.
- Open on a readable hook. Use one idea and CTA. Start the CTA at or after both 80% of the cut and the start of its final three seconds. Design vertical first and caption every cut.
- Link claims to proof, record asset rights and written likeness or voice permissions, and reject face swaps, misleading claims, endorsements, review gating, and dark patterns.
- Use HyperFrames 0.9.15 and local assets. Inspect lint, browser check, snapshots, real media, and independent QA before approval. Keep demo approval separate from client delivery.
- Keep working projects, vendor runtime copies, and rendered masters local. Retain reproducible source and sanitized evidence in Git.
- Run `python3 scripts/validate_repo.py` before every commit and delivery. Run `python3 scripts/verify_studio.py` before pushing.
