---
description: Render a HyperFrames ad project — lint, check, snapshot, then render to MP4
allowed-tools: Bash(npm ci), Bash(npx hyperframes:*), Bash(ffprobe:*), Bash(ffmpeg:*), Read, Glob
---

# /render-ad

Render a HyperFrames ad project to MP4. Arguments: `$ARGUMENTS` — the project
folder (for example `examples/hyperframes-diwali-8s` or
`outputs/<slug>/hyperframes`).

Example: `/render-ad examples/hyperframes-diwali-8s`

## Steps

1. Read `skills/ad-animation-motion/references/render-contract.md` first.
   Do not render from memory — follow the contract.
2. Set the environment traps first: render under the workspace, never /tmp.
   `export TMPDIR=$PWD/tmp` (create it under the workspace) and pass
   `--frames-cache-dir` under the workspace. For the legacy example and
   scaffolds, run `npm ci` to install the pinned CLI and prepare
   `assets/gsap.min.js` for local rendering.
3. Run the loop in order, fixing failures before moving on:
   `npx hyperframes lint`
   `npx hyperframes check --json`
   `npx hyperframes snapshot --at 0,1,3,5` — look at the PNG frames before rendering.
   `npx hyperframes render --quality looks -o <name>.mp4`
4. If the render fails, read the error, fix the project files, and retry.
   Common failures: disk gate (TMPDIR), `sub_timeline_script_failure`
   (CDN GSAP — vendor it locally), `first_frame_empty` (frame 0 must show
   the hook), `line_unread` (holds are 0.5s + 0.3s per word).
5. Verify the MP4 with `ffprobe` (duration, 1080x1920, fps) and report the
   file, duration, size, and ffprobe result. Never claim a render succeeded
   without the ffprobe output.
6. Use `--quality draft` to iterate and `--quality delivery` for the final.
