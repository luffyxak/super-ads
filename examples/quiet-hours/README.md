# Quiet Hours

HUSH Desk Mat is fictional. The [treatment](treatment.md) contains the three
concepts and selection rationale. The checked-in [evidence](evidence.json)
records the final local renders and a separate retake exercise. The studio
creates the original artwork, key-drop clip, planning reference, and percussion
locally through `make_assets.py`. Creative handoffs are labeled fixtures.

## Reproduce

From the root, after the README setup, use an unused storage folder.

```sh
python3 -m studio --data .studio/quiet-hours-demo demo
python3 -m studio --data .studio/quiet-hours-demo hook quiet-hours eviction
python3 -m studio --data .studio/quiet-hours-demo hook quiet-hours security
python3 -m studio --data .studio/quiet-hours-demo render quiet-hours
python3 examples/quiet-hours/verify_media.py --data .studio/quiet-hours-demo --output outputs/quiet-hours-media-check
python3 -m studio --data .studio/quiet-hours-demo report quiet-hours
python3 -m studio --data .studio/quiet-hours-demo materialize quiet-hours --output outputs/demo
```

With `--retake`, the media check changes the shot in its supplied workspace.
Use that flag on a disposable demo copy. The check exports a self-contained
starting reference, generates a local alternative MP4, imports and reattaches
it to the same shot ID, verifies reuse, and interrupts a separate render.

## Media and review

The final edited exports use H.264/AAC at 30 fps for 15 seconds. The hook is
visible at frame zero, the payoff caption begins at 9.133 seconds, and the
CTA begins at 12 seconds. Local browser verification checks full playback at
2× with audio enabled and muted, a midpoint seek, and timestamped frame
agreement. A separate Studio browser check uses the review player and compares
each downloaded file's SHA-256 to its manifest.

A cache-empty clean source run took 113.566 seconds and rendered all 15 shot instances.
The first full render after hook previews took 108.366 seconds with 14 shot
renders and one cache hit. The warm run took 5.150 seconds with 15 hits and
byte-identical masters. The isolated clip retake rendered three shot instances
(one per ratio), reused twelve, and reused audio in 41.853 seconds. Reported
times reflect this machine and cache state.

Independent review passed on the exact final master hashes. The reviewer
matched all 29 manifest entries and scored hook 8, clarity 8, pacing 7,
craft 8, brand fit 8, and rewatchability 7 out of 10. The 2.4–4.8s complaint
repeats the setup and the 9.133s payoff reads as a title. The final CTA shows
the full approved mat at 12 seconds in all three ratios. Human approval is
pending.

Rendered masters, working state, downloaded reports and browser captures
are local outputs. This example has no measured campaign performance.
