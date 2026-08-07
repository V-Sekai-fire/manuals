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

| RFD                                                                      | Title                                                                      | State      |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ---------- |
| [0000](0000-conventions/README.md)                                       | Conventions                                                                | published  |
| [0001](0001-zonefabric-roadmap-vs-mas-bandwidth-fps/README.md)           | Zonefabric roadmap: PERT order, current status, and fps/eBPF/sandbox notes | discussion |
| [0002](0002-taskweft-value-narrowing-primitives-and-refs/README.md)      | taskweft/nif's value narrowing: primitives, and refs as pointer strings    | discussion |
| [0003](0003-castspell-sandbox-package-and-manifest-encoding/README.md)   | CastSpell sandbox package format and manifest encoding                     | discussion |
| [0004](0004-castspell-libgodot-sandbox-runtime-scope/README.md)          | CastSpell's sandboxed runtime: embed `libgodot`, not `godot-sandbox`'s API | discussion |
| [0005](0005-gltf-interactivity-value-type-taxonomy-correction/README.md) | `gltf_interactivity`'s value types: primitive, `ref`, and `custom`         | discussion |
