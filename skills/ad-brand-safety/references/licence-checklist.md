# Licence checklist — reference for ad-brand-safety

## Claims
List every claim: price, discount, "best", "first", "No.1", "free",
"guaranteed". For each: proof and source. No proof, no claim. Cut the line.

## People
List every person: actor, creator, celebrity, child, voice. For each: consent
proof — contract, release, date, scope. No consent proof, no likeness.
No deepfake or face-swap of real people. This repo has no face-swap workflow.

## Asset licences (write licence + file name for each)
- Music, fonts, footage, stock, AI model outputs — keep proof in outputs/<slug>/.
- Fonts: OFL fonts are self-hosted; verify document.fonts.load resolves.
- Third-party repos: HyperFrames Apache-2.0 (no fees, no threshold);
  Remotion source-available, NOT open source — free for up to 3 people, a
  Company Licence is needed at 4+ people (headcount, not revenue);
  Paid cloud video APIs: per-provider terms, pricing, and commercial-use
  rights — check before spending;
  Stock footage: per-clip licence — keep source + licence + file name;
  lemo-opuscar MIT code, demo films CC BY 4.0; mg-styles-15 MIT;
  joeseesun/opus-video-prompts NO licence — do not reuse commercially.
- MoneyPrinterTurbo bundled music: never in a paid ad (YouTube-sourced,
  README-flagged). Stock footage per provider terms.

## Platform and India rules
Meta, YouTube, TikTok: claims, before/after, financial, health, alcohol,
gambling, children's ads. If a rule is unclear, cut the risky line.
India: ASCI guidelines, festive sensitivity, hallmark / BIS for gold,
UPI and financial claims. Accessibility: captions on, contrast, no flashing
at 3 per second or more, no text visible for under 0.5 seconds.

## Sign-off
Pass, pass with fixes, or fail — in writing, fixes listed by shot number.
No sign-off, no ship.
