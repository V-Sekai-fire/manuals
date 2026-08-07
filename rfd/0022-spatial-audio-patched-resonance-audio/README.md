---
title: "RFD 0022: Spatial audio via a patched Resonance Audio (HRTF and audio probes)"
state: published
scope: engine audio module (feat/module-resonance-audio)
---

## Decision

The zone server needs binaural HRTF rendering and audio probes for
occlusion, and Godot's built-in `AudioServer` gives neither. The
engine vendors a patched Resonance Audio as an engine module
(`feat/module-resonance-audio`), driven by a spatial-audio server
(`feat/spatial-audio-server`) that places sources and listeners and
resolves probes per frame. Google archived Resonance Audio upstream,
so the fork owns the code; the patch set rebases against no moving
upstream, and the module targets the frozen Godot 4.7 pin, so it does
not chase engine movement either. The `sponza-godot-audio` repo is the
demo and benchmark scene.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260606-spatial-audio-patched-resonance-audio.md`
- `sponza-godot-audio` demo repo
- Resonance Audio upstream (archived):
  <https://resonance-audio.github.io/resonance-audio/>

## Related

- `rfd/0020-pin-engine-to-frozen-godot-4-7`: fixes the engine API this
  module targets.
