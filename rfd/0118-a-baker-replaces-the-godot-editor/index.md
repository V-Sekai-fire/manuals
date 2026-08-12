---
title: "RFD 0118: A baker replaces the Godot editor"
rfd: "0118"
state: discussion
scope: client build pipeline, asset delivery, engine modules
---

## Problem

The Godot editor is a build-time dependency of every client artifact, and two steps are the reason.

Resource import turns `.png` into `.ctex`, `.wav` into a sample, and mesh formats into meshes, writing the results
under `res://.godot/imported/`. The importers live in `editor/`. Export builds the `.pck`, and `--export-release`
lives there too. A `template_release` binary reads what both produce and can run neither.

That places a GUI application in the middle of an automated pipeline. `godot-images` builds and publishes editors for
Windows and Linux so that CI can call `--export-release`, and `windows-editor.zip` alone is 482 MB. The assets
themselves already arrive at runtime from `fabric-asset-edge`, so the editor is doing work for content it never sees.

## Decision

**Bake to `.tscn` in the backend.** The text scene format is documented, and `ResourceFormatLoaderText` compiles into
every target. A baker that writes `.tscn` is writing a file the release template already knows how to load. The editor
is one program that happens to write the same format.

**Carry textures as Basis Universal inside glTF.** Import exists to choose a GPU format ahead of time. Basis
transcodes on the device, so the ahead-of-time step has nothing left to do. `KHR_texture_basisu` puts the texture
inside the glTF, and `GLTFDocument` loads it at runtime. `modules/basis_universal` and `modules/gltf` are already in
`fabric-godot-core`, and `godot-images` disables no modules on any platform.

**Run OpenUSD in the baker.** openUSD is a C++ library. `idtx-flow` calls it from an editor import plugin; the baker
calls the same library server-side and emits glTF and `.tscn`. This takes USD off artists' machines and out of the
engine.

**Mount the filesystem with a small C++ module in the release template.** A `PackSource` resolves `res://` against a
directory or against `fabric-asset-edge`'s content-addressed chunks. Register it at
`MODULE_INITIALIZATION_LEVEL_CORE`, because `PackedData` is core and has to be serving before anything asks for a
path. This has to be a module: GDExtension initializes after the filesystem is up, so it cannot serve boot.

**Keep gameplay out of the module.** Logic stays RISC-V ELF in the sandbox, as `zone-guest-godot` and
`zone-guest-middleham` already deliver it. The module is the one part of this stack that no CDN can replace, so every
line in it costs an engine release to change.

**Stop building the editor when the baker covers every asset class.** Until then `godot-images` keeps building it, and
`--export-release` stays available as a fallback.

## Consequences

The pipeline becomes scons for the template, the baker for the content, the module for the mount, and the sandbox for
the logic. No step needs a GUI, and no step needs a machine with the editor installed.

The module is the new failure surface. Three ways it fails quietly are recorded in `DETAILS.md`, and the first one
compiles, links, and resolves nothing.

## Open question

Whether a release template boots an unpacked project directory or requires a `.pck`. The module answers this by
construction once it exists. Until it does, the question is unsettled and a short experiment against
`linux-template-release` would settle it.

## References

- `v-sekai-multiplayer-fabric/fabric-godot-core`: the engine fork, and where the module lands under `modules/`
- `v-sekai-multiplayer-fabric/godot-images`: the engine builds, and the release that now carries templates alone
- `v-sekai-multiplayer-fabric/zone-client-godot`: a client that already ships `template_release` and no editor
- `v-sekai-multiplayer-fabric/zone-guest-godot`, `zone-guest-middleham`: the sandboxed guests the logic lives in
- `v-sekai-multiplayer-fabric/fabric-asset-edge`: the content-addressed store the pack source reads
- `v-sekai-multiplayer-fabric/idtx-flow`: the USD import the baker takes over

## Detail

{{< include DETAILS.md >}}
