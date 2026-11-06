# Realistic-footage limits — reference for ad-realistic-video

## The honest stack
HyperFrames and Remotion do motion graphics — proven on this machine.
Realistic footage in this repo comes from client-supplied clips or licensed
stock, composited in HyperFrames or Remotion — or, optionally, one shot from
a paid cloud video API. There is NO local GPU video model in this repo, and
nothing in the core stack needs a GPU. Do not recommend one.

## Route 1 — Client-supplied footage (best for the product moment)
- The supplied clip is the truth. Use it as shot; never regenerate the product.
- Check: resolution, frame rate, colour, sound, and that the label and logo
  are exactly right. If the clip is wrong, ask the client for a new one —
  do not fix a product shot with a generated clip.
- Keep the file name, source, and consent proof in `outputs/<slug>/`.

## Route 2 — Licensed stock (Pexels, Pixabay, Coverr)
- Search with the shot brief's keywords (subject + action + light + place).
  Get 3 candidate clips per shot and pick the best.
- Check the licence per clip — free stock is not licence-free. Keep the
  source, licence, and file name for every clip.
- Limits: stock is generic. It cannot show your exact product, your exact
  store, or your exact offer. Use it for atmosphere and B-roll (streets,
  homes, festivals, hands), never for the product close-up.
- Check every clip frame by frame: wrong text, wrong logos, wrong hands,
  wrong skin tones, watermarks. Cut what fails.

## Route 3 — Paid cloud video APIs (optional, one shot at a time)
- Kling, Veo, Runway, Luma, and similar services generate video in the cloud.
  They are paid third-party services — no local GPU needed, no install here,
  and this repo gives no install instructions for them because none were
  verified. Check each service's pricing, terms, and commercial-use rights
  yourself before spending.
- Use only for a shot no stock or supplied clip can cover. One shot at a
  time, 3 takes, pick the best.
- Limits: a generated clip is not proof the product looks right. Hands,
  faces, and text are known failure modes. Character consistency across
  clips is not guaranteed. Check the clip frame by frame before it goes
  near the ad. Never generate a real person without written consent.

## MoneyPrinterTurbo (harry0703/MoneyPrinterTurbo, v1.3.9, MIT code)
- Faceless-shorts factory, NOT an ad tool. No product shot, brand kit, CTA,
  storyboard, or exact-duration control. Fenced off: use only for
  hook/script/voiceover prototyping, or for render/assembly when all media is
  human-supplied. NEVER the paid hero ad. NEVER its bundled music in a paid
  ad — the bundled songs are YouTube-sourced and the README flags the
  copyright risk. Free path: Ollama + Edge TTS + Pexels/Pixabay/Coverr.
- Security: keys live in plaintext config.toml, API auth is off by default,
  default listen host is 0.0.0.0 — harden to 127.0.0.1 with an api_key.

## Rules for every realistic shot
One brief per shot. Three candidates or takes per shot, pick the best.
Lock character, wardrobe, and light across shots. Check hands, teeth,
text in frame, logos, and physics frame by frame. Never use a real person
without explicit written consent. No face-swap. No deepfake.
Composite in HyperFrames or Remotion; grade after the cut is locked.
