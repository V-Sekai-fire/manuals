# RFDs

Request-for-Discussion documents (format inspired by
[Oxide Computer Company's RFD process](https://rfd.shared.oxide.computer/),
the same format `weftspun/h2o-bench-tpcc` already used for its own
zonefabric RFDs before this repo ported a subset of them into
`decisions/` as MADR files).

This directory is a new, second record track alongside `decisions/`. The
project is moving gradually from MADR to RFD for new records, not
converting the existing MADR files. `decisions/` stays in use for now.
Use whichever track fits the record:

- `decisions/` (MADR, `YYYYMMDD-title.md`): a single point decision, one
  problem statement, one chosen option, dated.
- `rfd/` (this directory, `NNNN-title.md`): a longer-lived discussion
  document, numbered rather than dated, that can carry a proposal forward
  through a `State` and get amended over time.

## Adding an RFD

Create `rfd/NNNN-short-title.md`, using the next unused four-digit number
in this directory (check the table below, not `weftspun/h2o-bench-tpcc`'s
own RFD numbering, which is a separate sequence for a different repo).
Give the file this shape:

```markdown
# RFD NNNN: Title

**State:** prediscussion | discussion | published | committed

## Summary

## Background

## Motivation

## Proposal

## Recommendation and next steps

## Open questions and verification
```

`State` moves forward as the RFD matures: `prediscussion` while still being
drafted, `discussion` once open for review, `published` once the team
accepts the direction, `committed` once the work described is done.

## Index

| RFD                                                               | Title                                                                      | State      |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------- |
| [0001](0001-zonefabric-roadmap-vs-mas-bandwidth-fps.md)           | Zonefabric roadmap: PERT order, current status, and fps/eBPF/sandbox notes | discussion |
| [0002](0002-taskweft-value-narrowing-primitives-and-refs.md)      | taskweft/nif's value narrowing: primitives, and refs as pointer strings    | discussion |
| [0003](0003-castspell-sandbox-package-and-manifest-encoding.md)   | CastSpell sandbox package format and manifest encoding                     | discussion |
| [0004](0004-castspell-libgodot-sandbox-runtime-scope.md)          | CastSpell's sandboxed runtime: embed `libgodot`, not `godot-sandbox`'s API | discussion |
| [0005](0005-gltf-interactivity-value-type-taxonomy-correction.md) | `gltf_interactivity`'s value types: primitive, `ref`, and `custom`         | discussion |
