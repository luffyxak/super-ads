---
description: Scaffold a new ad brief, storyboard, prompts, and shot list from a brand and product
allowed-tools: Bash(python3 scripts/new_ad.py:*), Read, Write, Edit, Glob
---

# /new-ad

Scaffold a new ad for the user. Arguments: `$ARGUMENTS` — brand, product,
format (reel15 / tvc30 / launch10), festival (or none).

Example: `/new-ad Test Jewellers "Diwali gold bangles" reel15 Diwali`

## Steps

1. If any argument is missing (brand, product, format), ask for it. Do not
   guess the price, the offer date, or the store — those blanks stay blank
   until the user fills them.
2. Run the scaffolder (do not hand-write the files):
   `python3 scripts/new_ad.py --brand "<brand>" --product "<product>" --format <format> --festival <festival>`
3. With `--hyperframes`, also scaffold a HyperFrames project skeleton under
   `outputs/<slug>/hyperframes/` (index.html, compositions, and pinned npm setup).
   Without it, scaffold the brief/storyboard/prompts/shot-list only.
4. Tell the user the output folder and the next step: fill `brief.md`, then
   follow the matching workflow in `workflows/` (15s-reel, 30s-tvc, or
   product-launch).
5. Load `skills/ad-strategy` for the next step. Do not start creative work
   before the brief's five blanks are filled.
