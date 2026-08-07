# RFDs

Request-for-Discussion documents (format inspired by
[Oxide Computer Company's RFD process](https://rfd.shared.oxide.computer/),
the same format `weftspun/request-for-discussion` uses).

This directory is a second record track alongside `decisions/`. The
project migrates MADR files into `rfd/` gradually, not all at once; see
`rfd/0000-conventions/README.md`. A migrated MADR file gains a one-line
pointer to its new `rfd/NNNN` home, instead of being deleted.

- `decisions/` (MADR, `YYYYMMDD-title.md`): a single point decision, one
  problem statement, one chosen option, dated.
- `rfd/` (this directory, `NNNN-title/`): a longer-lived design record,
  numbered rather than dated, that can carry a proposal forward through
  a `State` and get amended over time.

## Adding an RFD

Create `rfd/NNNN-short-title/README.md`, using the next unused
four-digit number in this directory (check the table below, not
`weftspun/request-for-discussion`'s own numbering, a separate sequence
shared across other projects). Give the file this shape:

```markdown
---
title: "RFD NNNN: Title"
state: prediscussion
scope: one line naming the affected component
---

## Decision

## References

## Related
```

Keep `README.md` under 40 lines. Move a status table, a verification
log, or a deep walkthrough to a sibling `DETAILS.md` in the same
folder, and name it in one line under References.

`State` moves forward as the RFD matures: `prediscussion` while still
being drafted, `ideation` while exploring options before a proposal
firms up, `discussion` once open for review, `published` once the team
accepts the direction, `committed` once the work described is done,
`abandoned` if superseded or rejected, `moved` if the record relocated
elsewhere.

## Index

| RFD                                                                      | Title                                                                         | State         |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ------------- |
| [0000](0000-conventions/README.md)                                       | Conventions                                                                   | published     |
| [0001](0001-zonefabric-roadmap-vs-mas-bandwidth-fps/README.md)           | Zonefabric roadmap: PERT order, current status, and fps/eBPF/sandbox notes    | discussion    |
| [0002](0002-taskweft-value-narrowing-primitives-and-refs/README.md)      | taskweft/nif's value narrowing: primitives, and refs as pointer strings       | discussion    |
| [0003](0003-castspell-sandbox-package-and-manifest-encoding/README.md)   | CastSpell sandbox package format and manifest encoding                        | discussion    |
| [0004](0004-castspell-libgodot-sandbox-runtime-scope/README.md)          | CastSpell's sandboxed runtime: embed `libgodot`, not `godot-sandbox`'s API    | discussion    |
| [0005](0005-gltf-interactivity-value-type-taxonomy-correction/README.md) | `gltf_interactivity`'s value types: primitive, `ref`, and `custom`            | discussion    |
| [0006](0006-cockroachdb-with-mtls-role-separation/README.md)             | CockroachDB with mTLS and role-separated access                               | published     |
| [0007](0007-godot-double-precision-template-release-for-zone/README.md)  | Godot double precision template_release for zone servers                      | published     |
| [0008](0008-webtransport-over-quic-for-game-traffic/README.md)           | Use WebTransport over QUIC for game traffic                                   | published     |
| [0009](0009-ghcr-package-ownership-same-repo/README.md)                  | GHCR packages must be built by the repo that consumes them                    | published     |
| [0010](0010-maglev-cycle-1-gateway-handshake/README.md)                  | Godot client transport handshake against the authoritative server             | published     |
| [0011](0011-observability-stack-victoriatraces/README.md)                | Replace Jaeger with VictoriaTraces for trace storage                          | published     |
| [0012](0012-amend-pr-before-it-enters-the-queue/README.md)               | Amend a PR before it enters the merge queue, not after                        | published     |
| [0013](0013-archival-file-naming-convention/README.md)                   | Archival file naming convention for committed assets                          | published     |
| [0014](0014-art-game-loop-steel-thread/README.md)                        | Recursive art-game loop and its minimal steel thread                          | prediscussion |
| [0015](0015-bounded-llm-steering-queue/README.md)                        | Bound the LLM steering queue to avoid context overflow                        | published     |
| [0016](0016-checking-sccache/README.md)                                  | Checking the sccache build cache                                              | published     |
| [0017](0017-compiling-godot-engine/README.md)                            | Compiling the Godot engine                                                    | published     |
| [0018](0018-feature-classification-poc-baseline-stretch/README.md)       | Feature classification — proof of concept, baseline, stretch                  | published     |
| [0019](0019-gitassembly-tag-release/README.md)                           | Cut gitassembly tag releases for the assembled engine                         | published     |
| [0020](0020-pin-engine-to-frozen-godot-4-7/README.md)                    | Pin the engine to a frozen Godot 4.7 commit                                   | published     |
| [0021](0021-require-pr-and-merge-queue-on-main/README.md)                | Require pull requests and a merge queue on main                               | published     |
| [0022](0022-spatial-audio-patched-resonance-audio/README.md)             | Spatial audio via a patched Resonance Audio (HRTF and audio probes)           | published     |
| [0023](0023-webtransport-http3-transport/README.md)                      | WebTransport over HTTP/3 transport                                            | published     |
| [0024](0024-windows-background-services-nssm/README.md)                  | Running background services on Windows with nssm                              | published     |
| [0025](0025-tenseless-continuous-present-voice/README.md)                | Comments and docs use a tenseless continuous-present voice                    | published     |
| [0026](0026-commit-messages-sentence-case/README.md)                     | Commit messages use sentence case without Conventional Commits prefixes       | published     |
| [0027](0027-umbrella-package-installs-all-components/README.md)          | An umbrella package installs every component in one command                   | published     |
| [0028](0028-hexagonal-core-ports-adapters/README.md)                     | Hexagonal core/ports/adapters as the component convention                     | published     |
| [0029](0029-cassie-desktop-curvenet-authoring/README.md)                 | CASSIE desktop curvenet authoring for content, no Blender                     | published     |
| [0030](0030-cicd-runners-as-queueing-system/README.md)                   | CI/CD runners operate as a finite queueing system                             | published     |
| [0031](0031-content-build-merged-double-precision-mcp/README.md)         | Content creation in a single merged double-precision build via the editor MCP | published     |
| [0032](0032-core-codegen-lean-slang/README.md)                           | Core kernel codegen via lean-slang (Lean to Slang to SPIR-V)                  | published     |
| [0033](0033-core-contract-pure-reducer-byte-state/README.md)             | Cores as pure reducers over byte-serialized state                             | published     |
| [0034](0034-deterministic-cores-integer-seeded-rng/README.md)            | Deterministic cores via r128 fixed-point and seeded RNG                       | published     |
| [0035](0035-first-party-curated-content-zone-baker-budgets/README.md)    | First-party curated content with zone-baker budgets                           | published     |
| [0036](0036-forward-renderer-baked-light/README.md)                      | Forward renderer with baked light for the mobile floor                        | published     |
| [0037](0037-generated-behavior-sandboxed-riscv/README.md)                | Generated behavior runs as sandboxed RISC-V                                   | published     |
| [0038](0038-genre-generic-naming-no-trademarks/README.md)                | Genre-generic naming, no trademarked proper nouns                             | published     |
| [0039](0039-hexagon-budgeter-core/README.md)                             | Budgeter hexagon — core, ports, and adapters                                  | published     |
| [0040](0040-hexagon-combat-core/README.md)                               | Combat hexagon — core, ports, and adapters                                    | published     |
| [0041](0041-hexagon-loot-core/README.md)                                 | Loot hexagon — core, ports, and adapters                                      | published     |
| [0042](0042-hexagon-presence-core/README.md)                             | Presence hexagon — wrapping the existing presence stack                       | published     |
| [0043](0043-hexagon-progression-core/README.md)                          | Progression hexagon — core, ports, and adapters                               | published     |
| [0044](0044-lean4-kernel-cores-flat-c-host-adapters/README.md)           | Lean 4 build-time kernel cores with flat-C host adapters                      | published     |
