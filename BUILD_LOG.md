# Super Ads Creator v2 — Build Log

Built 5 Nov 2026 from five deep reads (skills-format, HyperFrames,
code-film, realistic-video, prompt-libs), each from a full local clone of
the repos, plus live render tests on this machine. All content in this repo
is original, inspired by patterns only. Third-party repos are referenced by
name + URL + licence + install command, never copied.

## What v2 is

- 11 skills (Anthropic Agent Skills format, frontmatter + per-skill
  `references/` + `LICENSE.txt`), 8 agents (YAML frontmatter), 3 slash
  commands (`/new-ad`, `/render-ad`, `/review-ad`), 6 workflows, 5 prompt
  files, 6 playbook docs, 3 written examples + 1 proven HyperFrames project,
  4 templates, 2 scripts, evals (test prompts + trigger eval set).
- Core stack (runs without a GPU): HyperFrames (primary, proven here) +
  Remotion (templates/versioning) + code-rendered lemo/mg patterns +
  MoneyPrinterTurbo fenced as prototyping only.
- Realistic footage: client-supplied clips or licensed stock (Pexels,
  Pixabay, Coverr), composited in HyperFrames/Remotion, or optionally one
  shot from a paid cloud video API (Kling, Veo, Runway, Luma).

## Test results

- `python3 scripts/validate_repo.py`: PASS, exit 0 (all checks, run 5 Nov 2026).
- `python3 scripts/new_ad.py --brand "Test Jewellers" --product "Diwali gold bangles" --format reel15 --festival Diwali`: PASS, exit 0 — created `outputs/test-jewellers-diwali-gold-bangles-diwali/` with brief.md, storyboard.md, prompts.md, shot-list.csv (test output deleted afterwards).
- `python3 scripts/new_ad.py ... --hyperframes`: PASS, exit 0 — additionally scaffolded `hyperframes/` (index.html, compositions/hook.html, product.html, cta.html, assets/gsap.min.js, hyperframes.json, package.json, README.md). The scaffolded project lints clean: `npx hyperframes lint` → 0 errors, 0 warnings.
- HyperFrames render of `examples/hyperframes-diwali-8s/`: PASS (see "Render test" below).
- Spot-check grep for the removed model name, its vendor, the old VRAM
  figures, and the stale clone host: zero hits in the repo.

## Render test

`examples/hyperframes-diwali-8s/` rendered on this machine (Node v24,
ffmpeg 8.1, HyperFrames CLI 0.9.15, no GPU) with `TMPDIR` under the
workspace and vendored GSAP, via lint → check --json → snapshot →
render. `npx hyperframes lint`: 0 errors, 0 warnings. `check --json`:
passed, exit 0. `snapshot --at 0,1,3,4,6,7.5`: 7 PNG frames + contact
sheet. Render: `--quality looks`, 240/240 frames, 28.4s wall time,
saved as `examples/hyperframes-diwali-8s/rendered-test.mp4` (511.7 KB).
ffprobe: H.264, 1080x1920, 30 fps, 240 frames, duration 8.000000s,
size 523945 bytes. Decoded frames at t=0/1/3/5/7s verified non-blank
(mean brightness 21.7–28.0 on the dark maroon field, distinct per beat).
Identical byte size to the original research render (523,945 bytes) —
the render is deterministic. See `examples/hyperframes-diwali-8s/README.md`
for the exact commands and the environment traps (TMPDIR, vendored GSAP).

## v1 errors fixed

1. `plugin.json` had `skills` and `agents` keys (silently ignored) and a
   plain-string author. Fixed: minimal manifest only (name, version,
   description, author object, license, keywords, homepage, repository).
   Added `.claude-plugin/marketplace.json` so it installs via marketplace add.
2. All 8 agents had no frontmatter. Fixed: YAML frontmatter with
   name/description/tools/model/color on every agent.
3. All 11 skill descriptions were 148–197 chars, one generic sentence.
   Fixed: 300–600 chars each, with concrete trigger phrases and DO-NOT
   boundaries, plus a `license: MIT` field and a `LICENSE.txt` per skill.
4. No progressive disclosure. Fixed: per-skill `references/` files; long
   playbooks live as skill references, not only at repo root.
5. The validator only checked "name + description present". Fixed: official
   rules — name == directory, kebab-case, 1–64 chars, description 300–1024
   chars, no angle brackets, unknown frontmatter keys rejected, YAML valid,
   SKILL.md under 500 lines, referenced files exist, agents have frontmatter,
   plugin.json has no skills/agents keys, marketplace.json exists, no
   placeholders, no banned wrong claims.
6. No evals. Fixed: `evals/` with with-skill vs baseline test prompts, a
   trigger eval set, and grading notes. No eval runs have been executed yet.
7. No slash commands. Fixed: `commands/new-ad.md`, `render-ad.md`,
   `review-ad.md` with description + allowed-tools frontmatter and $ARGUMENTS.
8. HyperFrames was called Python with a pip install. Fixed: TypeScript /
   Node 22+, installed with npx, Apache-2.0, no per-render fees. Added the
   render contract, the registry, the lint → check → snapshot → render loop,
   vertical numbers, measured motion values, and the TMPDIR + vendored-GSAP
   traps (both proven by the live render).
9. Remotion's paid threshold was stated as headcount-or-revenue. Fixed:
   headcount only — free for up to 3 people, Company Licence at 4+ people.
   Licence is source-available, NOT open source. Added Automators pricing
   and the no-upload-your-own-code rule.
10. The node-graph engine's clone URL pointed at the stale host. Fixed to
    the live host. (The engine itself was later removed from the main stack
    — see "Scope change" below.)
11. Video prompts assumed a realistic diffusion model as the default and
    had one tier only. Fixed: three tiers (one-line / template / full spec),
    code-rendered prompts first, realistic-footage prompts labelled, prompt
    anatomy (9 parts), banned list, self-check, cost/iteration note.
12. `mg-styles.md` was 15 invented styles with a palette and two motion
    sentences each. Fixed: 15 original styles in the 11-section style
    format with stack mapping, render settings, banned lists, and variation
    space. Styles are proven by a rendered frame + demo film, not prose —
    the proof pattern is `examples/hyperframes-diwali-8s/`.
13. Missing: treatment-first, "not the demo again" check, second-AI jury,
    fonts-first step, audio discipline (cue map, -14 LUFS measured),
    subtitle-hold rule, /tmp trap, deterministic-frames rule. All encoded
    in the animation skill, the render-contract reference, and the workflows.

## Scope change (applied during the v2 build)

The local GPU video model was removed entirely from v2, together with the
GPU-gated node-graph engine and all other local GPU video models that were
listed as replacements. Reason: the user does not want any high-RAM /
high-end GPU model in the repo. Removed: the model rows in
`docs/GITHUB_SOURCES.md`, the model sections in `docs/ANIMATION_GUIDE.md`,
all guidance in `skills/ad-realistic-video/` (rewritten as a realistic-
footage skill), the realistic-video prompt section in
`prompts/video-prompts.md` (rewritten as shot briefs for stock/supplied/
cloud-API footage), and mentions in README, CLAUDE.md, AGENTS.md, LICENSE,
agents, and skill references. Replaced with: (1) client-supplied / licensed
stock footage (Pexels, Pixabay, Coverr), composited in HyperFrames/Remotion;
(2) an optional paid cloud video API route (Kling, Veo, Runway, Luma —
named only as paid third-party services, no install instructions that were
not verified). No other local GPU model was substituted. The core v2 stack
runs without a GPU. Verified by grep over the whole repo: zero hits for the
removed model name, its vendor, the old VRAM figures, and the stale clone
host. (The validator keeps a guard for these strings, assembled at runtime
so the guard itself does not reintroduce them.)
