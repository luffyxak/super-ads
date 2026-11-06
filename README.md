# Super Ads Creator

> A one-stop repo to create production / commercial-ready social media ads with Claude Code / Codex.
> Drop it in, brief it, ship it. Vertical-first, hook-first, meme-able, brand-safe.

Built from studying 150+ booming ads (2010–2026) — India, USA, UK, Europe, Japan, Brazil,
Australia, Thailand — plus 53 Diwali ads, and the Moonshot / Tanmay Bhatt challenger school.
It also curates the best open animation + AI-video tooling on GitHub (10k+ stars for trust).

## Super Ads Studio quickstart

Run locally on macOS or Linux with Python 3.11+, Node 22+, and FFmpeg 7+ (including ffprobe).

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
npm ci
npx --no-install playwright install chromium
python3 scripts/verify_studio.py --doctor
python3 -m studio demo
python3 -m studio serve
```

Open [the local studio](http://127.0.0.1:8765), choose **Quiet Hours**, and use Brief, Storyboard, Review, and Delivery. This fictional example uses fixture handoffs and original local media. You can also start a blank workflow. The default workspace and imported assets are saved under `.studio/`.

```bash
python3 -m studio hook quiet-hours eviction
python3 -m studio hook quiet-hours security
python3 -m studio render quiet-hours
python3 -m studio report quiet-hours
python3 -m studio materialize quiet-hours
python3 scripts/verify_studio.py
```

Materialize writes a new `outputs/quiet-hours/` folder. Use `--output` with a different parent for a repeat export. Use the browser or `python3 -m studio act PROJECT ACTION PAYLOAD.json` for edits, review, and approvals. Browser and CLI share the database. The report is a draft until an independent review and a distinct human approval are recorded for the exact files. Client-ready delivery is disabled for fictional projects. On Debian/Ubuntu, install Chromium system dependencies with `npx --no-install playwright install --with-deps chromium`.

See [the harness](docs/HARNESS.md) for workflow, storage, provider, and release contracts and [the production specification](docs/STORYFORGE_PRODUCTION.md) for storyboard practices.

## What you get

- **11 skills** in `skills/` — strategy, creative direction, Gen-Z copy, visual design,
  video direction, motion, realistic video, social formats, Diwali/festive, brand safety,
  performance analysis. Anthropic Agent Skills format.
- **8 agents** in `agents/` — strategist, creative-director, copywriter, visual-designer,
  animator, video-director, editor, QA / brand-safety. Each has a role, inputs, outputs,
  handoff rules and a quality checklist.
- **6 workflows** in `workflows/` — 15s reel, 30s TVC, Diwali campaign, product launch,
  UGC creator, Super-Bowl-style. Each with steps, agents, skills, deliverables, time, QA gates.
- **Prompts** in `prompts/` — 12 original video prompts, image prompts, copy prompts,
  15 motion-graphic styles, product-launch prompts.
- **Playbooks** in `docs/` — learned patterns from 150+ ads, Moonshot playbook,
  Diwali playbook, country playbook, GitHub sources, animation guide.
- **Templates + examples** — brief, storyboard, shot-list, review checklist, plus 3 worked examples and a proven HyperFrames project (`examples/hyperframes-diwali-8s/` — 8s, 9:16, rendered here).
- **Commands** in `commands/` — `/new-ad`, `/render-ad`, `/review-ad` slash commands.
- **Evals** in `evals/` — test prompts (with-skill vs baseline) and a trigger eval set.
- **Scripts** — `new_ad.py` scaffolds a new ad; `validate_repo.py` checks the repo.

## The creative rules (encode these everywhere)

1. Hook in the first 1–2 seconds. No slow open. No logo card first.
2. One punch per ad. One idea, one joke, one feeling, one CTA.
3. 15–30 seconds, rewatchable. If it is not worth a second watch, cut it.
4. Celebrity subversion, not endorsement. Cast against type. The star is the joke, not the pitch.
5. The medium is the joke. The format, the platform, the trend — use it, do not fight it.
6. Challenger energy. Punch up. Small brand, big idea, honest voice.
7. Meme-able. One line, one frame, one sound that can be screenshotted and shared.
8. No hard sell in the first 80%. Earn the last 3 seconds. CTA only at the end.
9. 9:16 vertical first. Captions on. Safe zones respected. Sound-off must still work.
10. Brand safety + consent. No deepfake of a real person without explicit permission.
    No face-swap of real people. No misleading claims, no review gating, no dark patterns.
11. India: Hinglish, festive, family, Tier-2/3 clarity. Say it simply. Show it, do not explain it.
12. 50-year designer + Gen-Z creativity: craft is timeless, taste is now. Typography, timing,
    colour and sound matter as much as the idea.

## Quickstart — 5 minutes

```bash
git clone <your-fork> super-ads-creator
cd super-ads-creator
python3 scripts/validate_repo.py
python3 scripts/new_ad.py --brand "Test Jewellers" --product "Diwali gold bangles" --format reel15 --festival Diwali
```

Open `outputs/test-jewellers-diwali-gold-bangles/brief.md`, fill the 5 blanks,
then follow `workflows/15s-reel.md`.

In Claude Code, the repo's `CLAUDE.md` is auto-read. In Codex, read `AGENTS.md`.
Load only the skills you need for the step you are on — see `CLAUDE.md`.

## Team — how the 8 agents work together

```
Brief → Strategist → Creative Director → Copywriter → Visual Designer
      → Video Director → Animator → Editor → QA / Brand Safety → Ship
```

Text diagram:

- Strategist: who, why, one punch, proof, CTA. Output: 1-page strategy.
- Creative Director: 3 concepts, pick 1, kill 2. Output: concept board.
- Copywriter: hook, script, captions, 3 hook variants. Output: script + captions.
- Visual Designer: look, palette, type, key frames. Output: styleframes.
- Video Director: shots, camera, performance, sound. Output: shot list + director notes.
- Animator: motion, timing, transitions, text. Output: motion pass / Remotion / HyperFrames render.
- Editor: cut, captions, safe zones, sound mix, export. Output: 9:16 + 1:1 + 16:9 masters.
- QA / Brand Safety: claims, consent, licences, accessibility, platform rules. Output: sign-off.

No agent ships alone. QA is a gate, not a suggestion. See `agents/`.

## 3 example commands

```bash
# 1. Diwali 15s reel for jewellery
python3 scripts/new_ad.py --brand "Test Jewellers" --product "Diwali gold bangles" --format reel15 --festival Diwali

# 2. Moonshot-style 30s fintech ad
python3 scripts/new_ad.py --brand "PayQuick" --product "UPI in 2 taps" --format tvc30 --festival none

# 3. 10s product launch, no festival
python3 scripts/new_ad.py --brand "GlowSip" --product "Mango sparkling water" --format launch10 --festival none
```

Then run the matching workflow in `workflows/`.

## Install — animation / video tooling

You do not need everything on day one. Start with ffmpeg + Node + Python, add the rest
only when the workflow needs it. Full table, stars (Nov 2026 snapshot), licences and
install commands: `docs/GITHUB_SOURCES.md` and `docs/ANIMATION_GUIDE.md`.

```bash
# essentials
ffmpeg -version
node --version
python3 --version
npx create-video@latest  # Remotion is Node, not pip
```

Remotion (Node 20+, React — 70,893 stars, live-checked 5 Nov 2026) and HyperFrames
(TypeScript / Node 22+, HTML to MP4 — 79,214 stars, live-checked 5 Nov 2026) are the two
code-rendered paths. Realistic footage comes from supplied or licensed stock,
or an optional paid cloud video API — no local GPU model in this repo.
Full guidance in `docs/ANIMATION_GUIDE.md`.

## Safety / licences

- Original work in this repo: MIT — see `LICENSE`.
- Third-party repos are referenced by name + URL + star count + licence. They are NOT copied
  into this repo. Check each licence before commercial use.
- `joeseesun/opus-video-prompts` has no licence — do not reuse its prompts commercially.
- Remotion is source-available with a paid licence needed at 4+ people (headcount, not revenue).
- Deep-Live-Cam / face-swap tools: do NOT use for real people without explicit consent.
  This repo contains no face-swap code and no deepfake workflow.
- Never present a real person's likeness, voice or endorsement without written permission.
- Claims in ads must be true, provable, and in the brief. QA checks this.

## Folder map

```
skills/         11 skills, SKILL.md each (+ references/ + LICENSE.txt per skill)
agents/         8 agent definitions (YAML frontmatter: name/description/tools/model)
commands/       3 slash commands: new-ad, render-ad, review-ad
evals/          test prompts + trigger eval set (with-skill vs baseline)
prompts/        video (3 tiers), image, copy, motion styles, product launch
workflows/      6 end-to-end workflows
templates/      brief, storyboard, shot-list, review checklist
examples/       3 worked examples + hyperframes-diwali-8s (proven 8s render)
docs/           playbooks, GitHub sources, animation guide
scripts/        new_ad.py (incl. --hyperframes scaffold), validate_repo.py (official rules)
.github/        CI: validate on every push
```

## When to use what

- Need an idea fast? `workflows/15s-reel.md` + `skills/ad-strategy` + `skills/ad-creative-director`.
- Need a Diwali campaign? `workflows/diwali-campaign.md` + `docs/DIWALI_PLAYBOOK.md`.
- Need Moonshot energy? `docs/MOONSHOT_PLAYBOOK.md` + `examples/fintech-30s-moonshot-style.md`.
- Need motion? `skills/ad-animation-motion` + `prompts/mg-styles.md` + `docs/ANIMATION_GUIDE.md`.
- Need realistic video? `skills/ad-realistic-video` + `prompts/video-prompts.md`.

## What changed in v2

- Plugin manifest fixed: minimal `plugin.json` (no `skills`/`agents` keys —
  they are silently ignored) + `.claude-plugin/marketplace.json` so the repo
  installs via marketplace add.
- All 11 skills: frontmatter with name == directory, 300–600 char descriptions
  with trigger phrases and DO-NOT boundaries, `license: MIT`, per-skill
  `references/` (progressive disclosure) and `LICENSE.txt`.
- All 8 agents: YAML frontmatter (name/description/tools/model).
- New: `commands/` (`/new-ad`, `/render-ad`, `/review-ad`) and `evals/`
  (with-skill vs baseline test prompts + trigger eval set).
- Corrected facts: HyperFrames is TypeScript / Node 22+ (no pip package);
  Remotion's paid threshold is headcount (free up to 3 people, Company Licence
  at 4+ — no revenue test); the local GPU video model was removed entirely —
  realistic footage is supplied/licensed stock or an optional paid cloud API,
  and the core stack runs without a GPU.
- Realistic footage in v2 is client-supplied or licensed stock composited in
  HyperFrames/Remotion, or an optional paid cloud video API. No local GPU
  video model is part of this repo — the whole core stack runs without a GPU.
- Proven render in-repo: `examples/hyperframes-diwali-8s/` (8s, 1080x1920,
  30 fps, rendered on this machine).

## Contributing

For the planned studio extension, see the [StoryForge production specification](docs/STORYFORGE_PRODUCTION.md).

Add a new skill only if it has a distinct job, a clear trigger, and a quality bar.
Add a new example only if it is a full worked example, not a sketch.
Run `python3 scripts/validate_repo.py` before every commit.
