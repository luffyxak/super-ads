# Release checkpoint

| Slice | Evidence |
|---|---|
| Baseline | [Source audit](SOURCE_AUDIT.md), 11 scaffold regressions, saved 8-second MP4 full decode |
| Harness | [Architecture and workflow contracts](HARNESS.md), shared SQLite and browser/CLI, Codex CLI discovery of all 11 symlinked skill folders |
| Keyless verification | `python3 scripts/verify_studio.py` passed locally and from extracted staged source after a fresh venv and `npm ci`. 30 Python tests, 39 fixture evals, and a real Chromium workflow with imported media and file downloads |
| Dependencies | Root and legacy npm audits reported zero vulnerabilities. Staged Gitleaks scan found no leaks |
| Creative | [Quiet Hours treatment and reproduction](../examples/quiet-hours/README.md). Two hook previews, three verified masters, image/clip evidence, a local round trip, and timed review findings |
| Delivery | Local `outputs/quiet-hours` contains the draft Markdown and HTML reports, three masters, captions, and verified 29-file manifest |
| Release | See the [GitHub Actions workflow](https://github.com/luffyxak/super-ads/actions/workflows/validate.yml) for checks on each exact pushed SHA |

For continued work, run the verification command from the root and use a
disposable workspace for fixture edits and render experiments. The demo passed
technical, brand-safety, and independent creative QA. Human approval remains
pending. No live provider comparison or campaign launch took place.
