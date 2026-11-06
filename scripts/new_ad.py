#!/usr/bin/env python3
"""Scaffold a new ad.

Usage:
    python3 scripts/new_ad.py --brand "Test Jewellers" --product "Diwali gold bangles" --format reel15 --festival Diwali
    python3 scripts/new_ad.py --brand "Test Jewellers" --product "Diwali gold bangles" --format reel15 --festival Diwali --hyperframes

Creates outputs/<slug>/ with brief.md, storyboard.md, prompts.md, shot-list.csv
With --hyperframes, also scaffolds outputs/<slug>/hyperframes/ — a HyperFrames
project skeleton (index.html + compositions/ + pinned GSAP setup) based on the
proven pattern in examples/hyperframes-diwali-8s/.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "hyperframes-diwali-8s"
FORMATS = {
    "reel15": (15, 6, 10, 35, "15s-reel"),
    "tvc30": (30, 8, 20, 70, "30s-tvc"),
    "launch10": (10, 4, 6, 22, "product-launch"),
}


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if 0 < len(slug) <= 64:
        return slug
    digest = hashlib.sha256(text.encode()).hexdigest()[:12]
    return f"{slug[:48].rstrip('-') or 'ad'}-{digest}"


def display_text(value):
    if (
        not value.strip()
        or len(value) > 120
        or any(unicodedata.category(char) in {"Cc", "Cs", "Zl", "Zp"} for char in value)
    ):
        raise argparse.ArgumentTypeError("use 1–120 characters on one line without controls")
    return value.strip()


def markdown_text(value):
    return re.sub(r"([\\`*_\[\]{}()#+.!|~])", r"\\\1", escape(value, quote=False))


def cta_start(total):
    return max(total * 0.8, total - 3)


def scaffold_hyperframes(out, brand, product, duration_seconds):
    """Scaffold a HyperFrames project skeleton from the proven example.

    Structure mirrors examples/hyperframes-diwali-8s/: root index.html hosts
    three sub-compositions (hook / product / cta), each a paused GSAP
    timeline on window.__timelines, fromTo only, locally installed GSAP, bundled
    fonts (Montserrat / Playfair Display). Durations scale to the format.
    """
    hf = out / "hyperframes"
    (hf / "compositions").mkdir(parents=True)

    total = duration_seconds
    hook_d = 2
    cta_at = cta_start(total)
    prod_d = cta_at - hook_d
    cta_d = total - cta_at
    durations = {"hook": hook_d, "product": prod_d, "cta": cta_d}

    def scene(slug, title_lines, sub, title_size, top, sub_top):
        title = "<br />".join(escape(line) for line in title_lines)
        duration = durations[slug]
        subtitle_start = 0 if slug == "cta" else 0.3
        subtitle_duration = duration if slug == "cta" else min(2.2, duration - subtitle_start)
        subtitle_opacity = 1 if slug == "cta" else 0
        return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; text-align: center; font-family: Montserrat, sans-serif; }}
    .title {{
      position: absolute; top: {top}px; left: 0; width: 1080px;
      color: #fff8ec; font-family: "Playfair Display", serif;
      font-size: {title_size}px; font-weight: 700; line-height: 1.05;
    }}
    .sub {{
      position: absolute; top: {sub_top}px; left: 0; width: 1080px;
      color: #f5c04e; font-size: 52px; font-weight: 600;
    }}
  </style>
  <div id="root" data-composition-id="{slug}" data-width="1080" data-height="1920">
    <div id="{slug}-title" class="clip" data-start="0" data-duration="{duration:g}" data-track-index="0">
      <div class="title">{title}</div>
    </div>
    <div id="{slug}-sub" class="clip" data-start="{subtitle_start:g}" data-duration="{subtitle_duration:g}" data-track-index="1">
      <div class="sub">{escape(sub)}</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{slug}-title", {{ y: 20 }}, {{ y: 0, duration: 0.5, ease: "power4.out" }}, 0);
    tl.fromTo("#{slug}-sub", {{ opacity: {subtitle_opacity}, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power4.out" }}, {subtitle_start:g});
    window.__timelines["{slug}"] = tl;
  </script>
</template>
"""

    (hf / "compositions" / "hook.html").write_text(
        scene("hook", [brand, "is here"], "Like the festival itself", 150, 380, 720), encoding="utf-8")
    (hf / "compositions" / "product.html").write_text(
        scene("product", [product], "[OFFER — fill in from brief.md]", 132, 380, 760), encoding="utf-8")
    (hf / "compositions" / "cta.html").write_text(
        scene("cta", [brand], "Shop Now — [CTA from brief.md]", 110, 420, 640), encoding="utf-8")

    index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        margin: 0; width: 1080px; height: 1920px;
        overflow: hidden; background: #1c060d;
      }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      .bg {{
        position: absolute; inset: 0;
        background: radial-gradient(circle at 50% 30%, #5a1220 0%, #1c060d 62%);
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total}"
      data-width="1080"
      data-height="1920"
    >
      <div class="bg"></div>
      <div
        id="hook"
        data-composition-id="hook"
        data-composition-src="compositions/hook.html"
        data-start="0"
        data-duration="{hook_d}"
        data-track-index="0"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
      <div
        id="product"
        data-composition-id="product"
        data-composition-src="compositions/product.html"
        data-start="{hook_d}"
        data-duration="{prod_d}"
        data-track-index="1"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
      <div
        id="cta"
        data-composition-id="cta"
        data-composition-src="compositions/cta.html"
        data-start="{cta_at:g}"
        data-duration="{cta_d}"
        data-track-index="2"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (hf / "index.html").write_text(index, encoding="utf-8")
    for config in ("hyperframes.json", "package.json", "package-lock.json"):
        shutil.copyfile(EXAMPLE / config, hf / config)
    (hf / "meta.json").write_text(
        json.dumps({"id": slugify(brand), "name": slugify(brand)}) + "\n", encoding="utf-8")
    (hf / "README.md").write_text(
        f"# HyperFrames project — {markdown_text(brand)} / {markdown_text(product)}\n\n"
        "Scaffolded from the proven pattern in `examples/hyperframes-diwali-8s/`.\n"
        "Fill the [OFFER] and [CTA] placeholders from `../brief.md` first, then\n"
        "render. Read `skills/ad-animation-motion/references/render-contract.md`\n"
        "before editing compositions.\n\n"
        "## Render (from this folder)\n\n"
        "```bash\n"
        "npm ci\n"
        'mkdir -p "$PWD/tmp"\n'
        'export TMPDIR="$PWD/tmp"\n'
        "npm run lint\n"
        "npm run check -- --json\n"
        "npm run snapshot -- --at 0,1,3,5   # look at the frames first\n"
        "npm run render -- --quality looks -o " + slugify(brand) + "-" + slugify(product) + ".mp4\n"
        "```\n\n"
        "The npm setup copies pinned GSAP to `assets/gsap.min.js` for local use.\n"
        "Review the GSAP Standard License before using or distributing the project.\n"
        "Use local assets at render time. Fonts: only the bundled families resolve by name; anything\n"
        "else needs `@font-face` to a file in `assets/fonts/`.\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new ad")
    parser.add_argument("--brand", required=True, type=display_text, help="Brand name")
    parser.add_argument("--product", required=True, type=display_text, help="Product name")
    parser.add_argument("--format", required=True,
                        choices=FORMATS,
                        help="Format: reel15, tvc30, launch10")
    parser.add_argument("--festival", default="none", type=display_text,
                        help="Festival, e.g. Diwali, or none")
    parser.add_argument("--hyperframes", action="store_true",
                        help="Also scaffold a HyperFrames project skeleton under outputs/<slug>/hyperframes/")
    args = parser.parse_args()

    festival_part = slugify(args.festival) if args.festival.lower() != "none" else ""
    parts = [slugify(args.brand), slugify(args.product)]
    if festival_part:
        parts.append(festival_part)
    slug = "-".join(parts)
    outputs = ROOT / "outputs"
    out = outputs / slug
    try:
        if outputs.is_symlink():
            parser.error("outputs must be a directory inside the repository, not a symlink")
        outputs.mkdir(exist_ok=True)
        out.mkdir()
    except FileExistsError:
        parser.error(f"existing path blocks scaffold: {out.relative_to(ROOT)}")
    except OSError as exc:
        parser.error(f"could not create scaffold directory: {exc.strerror}")

    try:
        write_scaffold(out, args)
    except OSError as exc:
        shutil.rmtree(out)
        parser.error(f"could not write scaffold: {exc.strerror}")
    return 0


def write_scaffold(out, args):
    seconds, setup_end, twist_end, words, workflow = FORMATS[args.format]
    duration = f"{seconds} seconds"
    word_count = f"about {words} words"
    cta_at = cta_start(seconds)
    brand, product, festival = map(markdown_text, (args.brand, args.product, args.festival))

    brief = f"""# Ad Brief — {brand} / {product}

## 1. Brand
- Brand name: {brand}
- Product: {product}
- Price / offer: [FILL IN — price, discount, end date]
- Offer end date: [FILL IN]
- Store / link / app: [FILL IN]

## 2. Audience
- Who, in one line: [FILL IN]
- Where (city tier, language): [FILL IN]
- What they already believe: [FILL IN]
- Festival / event: {festival}

## 3. Problem
- Problem in one line: [FILL IN]
- Why does it hurt now? [FILL IN]

## 4. One punch
- Punch in 5 words max: [FILL IN]
- Proof (1 fact + source): [FILL IN]
- Enemy (what are we against?): [FILL IN]

## 5. CTA
- CTA in the last 3 seconds: [FILL IN]
- Where (link / store / app): [FILL IN]
- By when: [FILL IN]

## 6. Format
- Format: {args.format} ({duration})
- Festival: {festival}
- Workflow: see workflows/{workflow}.md

## 7. Success metric
- Primary metric (pick one): hook rate / hold rate / CTR / sales / footfall
- Target number: [FILL IN]
- Date range: [FILL IN]

## Creative rules
- Hook in first 1-2 seconds. One punch per ad. {duration}, rewatchable.
- Celebrity subversion, not endorsement. Medium is the joke. Challenger energy.
- No hard sell in first 80%. CTA in last 3 seconds.
- 9:16 vertical first. Captions on. Safe zones.
- No deepfake of real people without explicit written permission.
"""
    (out / "brief.md").write_text(brief, encoding="utf-8")

    storyboard = f"""# Storyboard — {brand} / {product} ({args.format}, {duration})

| Shot | Time | Visual | Audio | Caption | Notes |
|---|---|---|---|---|---|
| 1 | 0-2s | Hook frame: [FILL IN] | Hook line | Caption line | Hook frame |
| 2 | 2-{setup_end}s | Setup: [FILL IN] | Dialogue / music | Caption line | Setup |
| 3 | {setup_end}-{twist_end}s | Twist / demo: [FILL IN] | Dialogue / sound effect | Caption line | Twist |
| 4 | {twist_end}-{cta_at:g}s | Payoff: [FILL IN] | Music / silence | Caption line | Payoff |
| 5 | {cta_at:g}-{seconds}s | CTA: product + CTA text | CTA line / music out | CTA text on screen | CTA last 3 seconds |

## Notes
- Format: {args.format} ({duration}), script {word_count}
- Festival: {festival}
- Product appears once, clearly, in use, for 2-3 seconds.
- See templates/storyboard-template.md for the full template.
"""
    (out / "storyboard.md").write_text(storyboard, encoding="utf-8")

    prompts = f"""# Prompts — {brand} / {product}

## Video prompts
- Shot 1 (hook): "9:16 vertical, close-up, [hero] looks at camera, [emotion], [light], 24fps. Negative: no extra fingers, no warped faces, no morphing."
- Shot 2 (setup): "9:16 vertical, [scene], [action], [camera], [light], 24fps."
- Shot 3 (twist / demo): "9:16 vertical, [product] in use, [action], [light], 24fps. Negative: no warped label, no warped text."
- Shot 4 (payoff): "9:16 vertical, [reaction], [light], 24fps."
- Shot 5 (CTA): "9:16 vertical, [product] centre, CTA text space, [light], 24fps."

## Copy prompts
- Hooks: write 5 hooks, 6 words or fewer each, first 2 seconds.
- Script: {duration}, {word_count}, beats hook / setup / twist / payoff / CTA.
- Captions: 2 lines max, 32 characters per line, sound-off must work.

## Motion style
- Pick ONE style from prompts/mg-styles.md. One style per ad.
- Timing: 24 or 30 fps, 9:16, 1080x1920. Hook text in by 0.3s, out by 1.2s.

## Sources
- prompts/video-prompts.md — original prompts in three tiers (one-line / template / full spec), code-rendered first, realistic-video labelled
- prompts/image-prompts.md — styleframes and thumbnails
- prompts/copy-prompts.md — hooks, scripts, captions
- prompts/mg-styles.md — 15 original motion styles
"""
    (out / "prompts.md").write_text(prompts, encoding="utf-8")

    shot_csv = f"""shot,time,shot_size,camera,action,line,sound,duration_seconds,notes
1,0-2s,Close-up,Static,"Hook: hero looks at camera",Hook line,Music in,2,Hook frame
2,2-{setup_end}s,Wide,Slow push-in,"Setup: problem appears",Dialogue,Music,{setup_end - 2},Setup
3,{setup_end}-{twist_end}s,Medium,Track,"Twist: product / demo",Dialogue / sound effect,Sound effect,{twist_end - setup_end},Twist
4,{twist_end}-{cta_at:g}s,Close-up,Static,"Payoff: reaction",Payoff line,Music / silence,{cta_at - twist_end:g},Payoff
5,{cta_at:g}-{seconds}s,Close-up product,Static,"Product in hand, CTA text",CTA line,Music out,{seconds - cta_at:g},CTA last 3 seconds
"""
    (out / "shot-list.csv").write_text(shot_csv, encoding="utf-8")

    if args.hyperframes:
        scaffold_hyperframes(out, args.brand, args.product, seconds)

    print(f"Created {out}/")
    print("  brief.md")
    print("  storyboard.md")
    print("  prompts.md")
    print("  shot-list.csv")
    if args.hyperframes:
        print("  hyperframes/ (index.html, compositions/, pinned npm setup, README.md)")
    print(f"Next: fill brief.md, then follow workflows/{workflow}.md")


if __name__ == "__main__":
    sys.exit(main())
