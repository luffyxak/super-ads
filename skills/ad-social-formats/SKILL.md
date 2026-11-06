---
name: ad-social-formats
description: >-
  Format ads correctly for Instagram Reels, YouTube Shorts, TikTok, and Meta: 9:16, 1:1, 16:9, safe zones, captions, thumbnails. Use before every export, when text is cut off or captions are hidden by platform UI, or when one master must become three cuts. Trigger phrases: 'export the ad', 'safe zones', 'make the 1:1 cut', 'thumbnail', 'captions on'. Delivers three masters, captions, and a thumbnail. Do NOT use for creative concepts or motion — this skill only formats and exports finished work.
license: MIT
---
# Ad Social Formats

## When to use
- Before export, every time. Format is not an afterthought.
- When text is cut off, faces are cropped, or captions are hidden by platform UI.
- When one master must become three cuts: 9:16, 1:1, 16:9.

## Workflow
1. Master in 9:16 vertical first: 1080x1920, 24 or 30 fps, H.264, AAC audio.
   This is the format the audience actually sees. Design for it first.
2. Respect safe zones (1080x1920): top 168px clear, all words and product inside
   the 168–1330px band, below 1330px only texture and decoration. Minimum 28px type,
   about 5 words per claim line. Platform UI covers the bottom (caption, buttons)
   and the top (profile, sound). Test on a real phone, not only on a desktop preview.
3. Captions on, always. Burned-in captions for Reels / Shorts / TikTok, plus an SRT file.
   Two lines max, 32 characters per line, high contrast, readable sound-off.
4. Make the 1:1 cut (1080x1080) by reframing, not by stretching. Centre the hero.
   Make the 16:9 cut (1920x1080) the same way. Check every cut on a phone.
5. Thumbnail: one frame, hook text, hero face or product, high contrast.
   The thumbnail is a poster, not a random frame. Pick it deliberately.
6. Sound: -14 LUFS for social, peaks below -1 dB. Music must not drown the hook line.
7. Export checklist: file name `<slug>-9x16.mp4`, `<slug>-1x1.mp4`, `<slug>-16x9.mp4`,
   captions `.srt`, thumbnail `.jpg`, duration, size, fps in the delivery note.
8. Hand off to QA with all three cuts and the thumbnail.

## Output format
- Masters: 9:16, 1:1, 16:9 — file names, sizes, durations
- Safe-zone check: pass / fail per cut, with a phone screenshot note
- Captions: burned-in yes/no, SRT file name
- Thumbnail: file name + why this frame
- Sound: LUFS, peak, music licence note

## Quality bar
- No text is hidden by platform UI in any cut.
- The hook is readable sound-off in 1 second.
- The 1:1 and 16:9 cuts are reframed, not stretched or letterboxed by accident.
- File sizes are reasonable for upload: 9:16 15s is typically under 30 MB at good quality.

## Examples
- Reel 15s: 1080x1920, 30fps, captions burned-in, CTA text in the last 3 seconds, safe zone respected.
- Shorts 30s: same master, different thumbnail and title, no platform watermark.
- Meta feed 1:1: centre crop, hero in the middle third, captions still readable.

## Anti-patterns
- Designing in 16:9 and cropping to 9:16 at the end. Design vertical first.
- Text at the very bottom where the caption and buttons sit.
- No captions. Half the audience watches sound-off.
- A thumbnail that is a blurry mid-action frame.

## References
- `references/vertical-safe-zones.md` — Vertical safe zones — the 168-1330px text band, type sizes, caption rules, export checklist.
- Read only the reference file for the step you are on; do not load every reference at once.
