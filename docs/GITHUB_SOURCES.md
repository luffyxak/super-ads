# GitHub Sources — Repos to Learn From

Star counts marked "live-checked 5 Nov 2026" were read from the GitHub API on
5 Nov 2026. All other counts are a November 2026 snapshot — re-verify live
before you trust a number; stars change daily. Licences change too — check the
licence file in the repo before commercial use.
This repo does NOT copy code or prompts from these repos. It references them.
All content here is original, inspired by patterns only.

## How to read this table

- Stars: a trust / quality signal, not a guarantee. 10k+ stars is the bar used here.
- Licence: check it yourself before commercial use. "No licence" means do not reuse commercially.
- Use-for-ads: what this repo is actually good for in an ad workflow.

## Agent / skills orchestration

| Repo | URL | Stars | Licence | Install | Use for ads |
|---|---|---|---|---|---|
| anthropics/skills | https://github.com/anthropics/skills | 187,568 (live-checked 5 Nov 2026) | MIT (most skills; check each skill folder) | `git clone https://github.com/anthropics/skills.git` | Agent Skills format — the format this repo follows. Learn the structure, write your own skills. |
| HyperFrames | https://github.com/heygen-com/hyperframes | 79,214 (live-checked 5 Nov 2026) | Apache-2.0 — no per-render fees, no commercial-use threshold | `npx hyperframes` / `npx skills add heygen-com/hyperframes` | Code-rendered video in TypeScript / Node 22+ (HTML to MP4). Primary renderer for this repo. Skills + registry first. |
| Remotion | https://github.com/remotion-dev/remotion | 70,893 (live-checked 5 Nov 2026) | Source-available, NOT open source — free for up to 3 people; Company Licence needed at 4+ people (headcount, not revenue) | `npx create-video@latest` | Code-rendered video in React. Templates, versions, price/city/language swaps. |
| MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | 139,492 (live-checked 5 Nov 2026) | MIT (code only; assets are a licence patchwork) | `pip install mpt && mpt webui` | Faceless-shorts factory. Prototyping and assembly ONLY — never the paid hero ad, never its bundled music. |

## Animation / motion — the code-film repos

| Repo | URL | Stars | Licence | Use for ads |
|---|---|---|---|---|
| lemo-opuscar | https://github.com/lemomo-ai/lemo-opuscar | 12,443 (live-checked 5 Nov 2026) | MIT (code/docs); demo films/stills CC BY 4.0 | 66 code-made film styles, each an 11-section STYLE.md. The style format this repo's `prompts/mg-styles.md` follows. Node 20+, ffmpeg 7+, Python 3.11+. |
| mg-styles-15 | https://github.com/Vincentwei1021/mg-styles-15 | Nov 2026 snapshot — check repo | MIT (code/prompts/films); samples CC0/PD | 15 motion-graphic styles, each a 10s film with full prompt and source. The prompt template this repo follows. Node 22.12+, Chrome, ffmpeg, Python 3.11+. |
| ClaudeAnimationBase | https://github.com/JohnHeibel/ClaudeAnimationBase | Nov 2026 snapshot — check repo | MIT | Hand-painted Clawd cartoons in p5.js + p5.brush. Storyboard-first animation method. Needs a GPU for watercolour frames in reasonable time. |
| pdoom-video | https://github.com/mexicat/pdoom-video | Nov 2026 snapshot — check repo | MIT (code); song + lyrics NOT covered | Code-rendered music video, TypeScript + three.js. Word-synced karaoke typography, beat-synced cuts. Needs real Chrome + GPU + ~23 GB RAM for a full render. |

## Prompt libraries — patterns only, never copied text

| Repo | URL | Stars | Licence | Use for ads |
|---|---|---|---|---|
| awesome-opus5-5-videos (yihui-dev) | https://github.com/yihui-dev/awesome-opus5-5-videos | Nov 2026 snapshot — check repo | MIT (repo); each prompt belongs to its creator | 703 code-rendered video prompts. Learn the three prompt tiers (one-line / template / spec). Never copy a prompt. |
| awesome-opus-5-5-videos (athemeroy) | https://github.com/athemeroy/awesome-opus-5-5-videos | Nov 2026 snapshot — check repo | CC BY 4.0 (its own writing only; third-party material excluded) | Research collection: 71.6% of ad/launch files are motion graphics/UI. Cite findings with attribution. |
| opus-video-prompts (joeseesun) | https://github.com/joeseesun/opus-video-prompts | Nov 2026 snapshot — check repo | **No licence stated — do NOT reuse commercially** | 18 prompts + 54 cases. Learn the shapes (one-liner / template / spec) only. Write all our prompts from scratch. |

## More Gen-AI / realistic video repos to research

- Realistic footage: client-supplied clips, licensed stock (Pexels, Pixabay, Coverr), or an optional paid cloud video API (Kling, Veo, Runway, Luma). No local GPU video model is part of this repo.
- Image models: Stable Diffusion / Flux / SDXL — check licence for commercial use.
- Face / voice: do NOT use face-swap / Deep-Live-Cam on real people without explicit consent.
  This repo has no face-swap workflow. If a repo is a face-swap tool, learn the warning, not the tool.
- Agent orchestration: Claude Code skills, Codex, LangGraph, CrewAI — learn the orchestration pattern,
  write your own agents in `agents/`.

## Warnings

- No licence = do not reuse commercially. Write original work.
- Remotion: free for up to 3 people; Company Licence needed at 4+ people (headcount, not revenue).
- HyperFrames: Apache-2.0, no fees, no threshold. There is no pip package.
- Paid cloud video APIs: per-provider terms, pricing, and commercial-use rights — check before spending. A generated clip is not proof the product looks right.
- Stock footage: per-clip licence; keep source + licence + file name for every clip.
- MoneyPrinterTurbo: never the paid hero ad, never its bundled music in a paid ad.
- Model licences: a model can be open for research and restricted for commercial use. Check.
- Celebrity / real-person likeness: no repo licence gives you consent. Get written consent separately.
- Star count is a signal, not a guarantee. Read the README, the issues, and the licence.
