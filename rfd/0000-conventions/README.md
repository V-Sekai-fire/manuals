---
title: "RFD 0000: Conventions"
state: published
scope: all files
---

## Decision

This repository writes Request-for-Discussion documents in the Oxide
style, the same style `weftspun/request-for-discussion` uses. Each RFD
lives in its own folder, `rfd/NNNN-kebab-title/`, not a single flat
file. Each RFD has a state: prediscussion, ideation, discussion,
published, committed, abandoned, or moved.

The repository writes prose in ASD-STE100 Simplified Technical
English. Code and identifiers do not follow STE. STE applies to
documents, comments, and user-visible text.

The repository keeps designs in one place. `decisions/` holds MADR
records, one point decision each, dated. An RFD points to a MADR, a
source file, or another RFD. It does not copy the source.

Each RFD's `README.md` stays under 40 lines. It states the state, the
scope, and the decision, in the fewest lines that keep all three true.
A measurement, a verification log, a status table, or a deep
walkthrough does not fit. Move it to a sibling file, `DETAILS.md`, in
the same RFD folder. The `README.md` names that file in one line.

`decisions/` (MADR, `YYYYMMDD-title.md`) still records a single point
decision. `rfd/` records a longer-lived design that can carry a
proposal forward and get amended over time. The project migrates
existing MADR files into `rfd/` gradually; a MADR file gains a
one-line pointer to its new `rfd/NNNN` home once migrated, instead of
being deleted.

## References

- RFD style: `weftspun/request-for-discussion`, `0000-conventions`
- STE spec: https://www.asd-ste100.org/
- STE linter: the `simplified-technical-english` Claude Code plugin

## Related

See `rfd/README.md` for the index and the numbering rule.
