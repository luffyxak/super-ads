# Image Prompts — Styleframes, Thumbnails, Key Visuals

Use for styleframes, thumbnails, posters and key visuals. 9:16 first, then 1:1.
Describe light, framing and feeling — not just the subject.

## Styleframe prompts
1. Hook frame: "9:16, close-up, [hero] looks directly at camera, deadpan, bold background [colour], hard light, centre framing, high contrast, thumbnail-ready."
2. Twist frame: "9:16, wide, [chaos / surprise moment], [hero] in the centre third, warm light, motion blur on background only, cinematic."
3. Payoff frame: "9:16, close-up, [product] in hand, warm light, shallow depth of field, gold / hero colour pops, clean background."
4. Family frame: "9:16, warm Indian home, family around a table, diya light, everyone laughing, natural skin tones, cinematic, 9:16."
5. Product hero: "9:16, product centre on [colour] background, soft studio light, condensation / texture detail, premium, no text, no props that distract."

## Thumbnail prompts
- "9:16 thumbnail, [hero face] + [product], bold hook text space at top, high contrast, one clear emotion, no clutter."
- "1:1 thumbnail, [product] centre, hero colour background, large readable hook text, clean."
- Always leave space for text: top 10% and bottom 20% are safe-zone aware. Do not put a face where the CTA will sit.

## Negative prompts for images
"No extra fingers, no warped faces, no warped text, no plastic skin, no extra limbs, no distorted logos, no watermark."

## Consistency
Use the same character lock as video: same age, hair, wardrobe, skin tone, light.
Generate 3 takes, pick the best. If the face changes, regenerate with the same seed.

## Colour notes
- Diwali: deep maroon #7A1F2B, gold #D4A017, cream #FFF6E5.
- Fintech challenger: black #111111, yellow #FFD400, white #FFFFFF.
- Premium: cream, gold, deep green. No neon unless the joke needs it.
- Skin tones: warm, real, not over-smoothed. Test on a phone in sunlight.

## What to avoid
- Stock-looking frames with no point of view.
- A product floating on a white background with no story.
- Text in the image that is spelled wrong. AI text is risky — check every letter, or add text in post.
- A thumbnail that is a blurry mid-action frame. Pick a deliberate frame.

## Reference-image workflow
Supply a reference image or clip and ask for a transformation — redraw as
line art, restyle, extend. The reference does the describing.
"Using the attached pack shot as the only product reference, rebuild it as a
flat line-art animation; keep the label exactly as supplied, do not redraw
the logo."
Rule: the supplied asset is the truth. The model animates around it, never
invents the product. If the logo or label changes, the frame fails.

## Brand-asset input spec (supply before generation)
- Pack shot / product photo: file name, angle, lighting, background.
- Logo: file name, exact colours, clear-space rules. Never redraw the logo.
- Brand colours: hex codes, 3 max. Brand fonts: file names + licences.
- Reference images: file names, what each one is for.
- Music / voice: track file or TTS voice + language.
Without these files, do not generate — ask for them first.
