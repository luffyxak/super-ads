# Super Ads Studio

Super Ads Studio is a local-first video production workspace for ad creatives,
editors, and small teams. Keep the campaign brief, storyboard, media, and
review history together as an idea moves from its first concept to delivery.

The browser editor and CLI share the same projects. You can produce and
render the included demo without an API key, or use the repository's agent
guides to bring Claude Code or Codex into the workflow.

[Features](#features) · [Quickstart](#quickstart) · [Documentation](#documentation)

![Super Ads Studio storyboard showing the Quiet Hours campaign, shot timeline, and editable shot inspector](docs/images/studio-storyboard.png)

*The included fictional Quiet Hours campaign, open in Storyboard.*

## Features

- **Plan the campaign.** Capture the audience, offer, product claims, and
  supporting proof. Compare concepts and choose a workflow for a reel, TVC,
  Diwali campaign, product launch, creator UGC, or big-event ad.
- **Edit shot by shot.** Set timing and captions on the storyboard, compare
  up to three opening hooks, and bring in images, clips, and audio. Replace a
  shot while keeping the rest of the timeline in place.
- **Review the cut.** Play each aspect ratio with safe-zone overlays, add
  timecoded feedback, and track asset rights and QA. Approval is tied to
  the reviewed version and its export hashes.
- **Package the delivery.** Render 1080p H.264 MP4s in vertical (9:16),
  square (1:1), and landscape (16:9). Export SRT captions, thumbnails,
  production reports, and a file manifest alongside the cuts.

HyperFrames renders each shot locally. A retake can reuse cached renders
for the shots you left alone.

## Quickstart

You’ll need Python 3.11+, Node 22+, and FFmpeg 7+ with `ffprobe` on macOS or Linux.

Run these commands from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
npm ci
npx --no-install playwright install chromium
python3 -m studio demo
python3 -m studio serve
```

After the server starts, open the address printed in your terminal and select
**Quiet Hours**. The demo includes five editable shots, two opening hooks, and
original artwork and audio. Choose **New campaign** to start with your own brief.

Projects and imported media are stored under `.studio/`.

<details>
<summary>CLI rendering and verification</summary>

Render a hook preview and save the demo cuts and report.

```bash
python3 -m studio hook quiet-hours eviction
python3 -m studio render quiet-hours
python3 -m studio report quiet-hours
python3 -m studio materialize quiet-hours
```

The files are saved in `outputs/quiet-hours/`.
Choose a new destination with `materialize --output` for repeat exports.
See the [demo guide](examples/quiet-hours/README.md)
for reproduction steps and measured render results.

Run the local checks with these commands.

```bash
python3 scripts/verify_studio.py --doctor
python3 scripts/verify_studio.py
```

On Debian or Ubuntu, install Chromium system dependencies with
`npx --no-install playwright install --with-deps chromium`.

</details>

## Documentation

| Guide | What it covers |
| --- | --- |
| [Campaign workflows](workflows/) | Reel, TVC, Diwali, launch, UGC, and big-event formats |
| [Production guide](docs/STORYFORGE_PRODUCTION.md) | Storyboards, continuity, shot retakes, clips, and audio |
| [Studio architecture](docs/HARNESS.md) | Local storage, agent handoffs, and release approvals |
| [Release evidence](docs/PROGRESS.md) | Test results, rendering checks, and delivery evidence |

For agent workflows, start with [AGENTS.md](AGENTS.md) or [CLAUDE.md](CLAUDE.md).

[MIT license](LICENSE)
