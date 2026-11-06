# StoryForge production patterns for Super Ads Studio

This specification extends the Super Ads Studio build. The existing role order,
workflow rules, HyperFrames render contract, and QA sign-off still govern delivery.

## Reference implementation

Inspect a local checkout of the original `storyforge-studio` project if available.
Start with its architecture, customization, Flow, research, and test-result
documents, then read the relevant scene editor and renderer tests.

The three upstream research references inform distinct areas:

- [OpenMontage](https://github.com/calesthio/OpenMontage/tree/d21f5d4eaa08422b09c7091757a05affcbabb35b) informed staged artifacts, a living storyboard, and review. Use it as an AGPL research reference without incorporating its source or assets.
- [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase/tree/0ac8bf2b31942376cb6b8c4074715595d512acd2) informed original character acting, timed poses, and frame strips. Use original Super Ads characters and artwork.
- [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar/tree/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00) informed exact-time preview, motivated camera movement, and sound cues. Use the existing Super Ads motion and render skills to implement these ideas.

## Studio requirements

1. **Living storyboard.** Give every shot a stable ID and typed, editable
   timing, action, visual, caption, sound, and evidence fields. Let the user
   scrub, reorder, preview, and replace shots. Use a shared scene description
   for editor preview and export. Keep planning references separate from assets
   that render. Show the actual final frame beside a planning reference.
2. **Product and character continuity.** Give assets explicit roles, including
   reference, packshot, background, character or mascot, external clip, and
   audio. Lock approved product appearance, packaging and logos per revision.
   Add simple editable cutout motion and expression cues where the brief calls
   for a mascot. Preserve the distinction between a flat image and a layered rig.
   Include the rights and consent record wherever the asset is referenced.
3. **Shot retakes and variants.** Render a shot or hook preview before a full cut.
   Cache validated shot renders by render-relevant inputs, asset bytes, renderer
   version and settings. Keep assembly and audio dependencies separate from
   picture. Allow 2–3 bounded variants that change a named variable, such as the
   opening hook, while sharing unchanged footage, proof, and offer terms.
   Invalidate affected deliveries and approvals when any approved input changes.
4. **Manual reference-to-clip workflow.** Export a self-contained starting frame
   or reference sheet, shot prompt, duration and aspect notes. Let the operator
   generate externally, then safely import, trim, preview and replace that shot.
   Preserve source, usage rights, disclosure, and the local scene revision.
   External generation is optional. Preserve any required watermarks.
5. **Audio and review.** Support local voice, score, and foley tracks, with
   timeline attachment, trimming, gain, fades, and sound-off review. Collect
   contact sheets, short action strips, technical media evidence, timecoded QA
   notes, and the human approval record with each delivery.

## Verification

Use the required fictional 15-second ad as the vertical slice. In a clean local
run, preview and edit a shot, import one licensed or original piece of artwork
and one clip, export a self-contained reference, produce two hook previews,
and render the approved demo in all three ratios. Verify that planning-only
artwork never enters the video, the intended source clip and product artwork
appear in decoded output, preview and export agree at chosen frames, a changed
asset invalidates the correct shot cache, unaffected shots reuse cached footage,
and old approvals cannot release a revised bundle. Record cold and warm render
times, shots rerendered, and real test evidence. Keep optional external generation
outside default CI and label any fixture-backed test.
