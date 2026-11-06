# Vertical safe zones — reference for ad-social-formats

## The numbers (1080x1920, from the HyperFrames vertical type reference)
- Top 168px: clear. Nothing there — platform UI covers it.
- Text band 168-1330px: all words and product live here.
- Below 1330px: texture and decoration only. No text under the right-hand
  action rail.
- Minimum 28px type. About 5 words max per claim line — cut words, never shrink.
- Frame 0 is the thumbnail: face, result, or one bold line already on screen.
  Never black, never a logo.

## Captions
Burned-in captions for Reels, Shorts, and TikTok, plus an SRT file. Two lines
max, 32 characters per line, high contrast, readable sound-off. Subtitle hold
at least max(1.8s, speech + 0.6s).

## Cuts
Master in 9:16 first: 1080x1920, 24 or 30 fps, H.264, AAC. Make the 1:1 cut
(1080x1080) and the 16:9 cut (1920x1080) by reframing, never by stretching.
Centre the hero. Check every cut on a real phone, not only on desktop.

## Sound
-14 LUFS for social, peaks below -1 dB. Music must not drown the hook line.

## Export names
`<slug>-9x16.mp4`, `<slug>-1x1.mp4`, `<slug>-16x9.mp4`, plus
`<slug>-captions.srt` and `<slug>-thumbnail.jpg`. File sizes: a 9:16 15s ad
is typically under 30 MB at good quality.
