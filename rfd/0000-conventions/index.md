---
title: "RFD 0000: Conventions"
rfd: "0000"
state: published
scope: all files
---

## Decision

This repository writes Request-for-Discussion documents in the Oxide
style, the same style `weftspun/request-for-discussion` uses. Each RFD
lives in its own folder, `rfd/NNNN-kebab-title/`, not a single flat
file. Each RFD has a state: prediscussion, ideation, discussion,
published, committed, abandoned, or moved.

Each RFD's `index.md` has a `## Problem` section before `## Decision`.
The `## Problem` section states, in one short paragraph, what is wrong
or missing today, and why that matters. A reader must understand the
problem before they read the decision.

Quarto renders the folder through `index.md`, and its frontmatter
carries the title, the number, the state, and the scope.

The repository writes prose in ASD-STE100 Simplified Technical
English. Code and identifiers do not follow STE. STE applies to
documents, comments, and user-visible text.

The repository keeps designs in one place. `decisions/` holds MADR
records, one point decision each, dated. An RFD points to a MADR, a
source file, or another RFD. It does not copy the source.

A section belongs in `index.md` when a reader needs it to reach the
decision. A measurement, a verification log, a status table, or a deep
walkthrough goes to a sibling file, `DETAILS.md`, in the same RFD
folder. The `index.md` names that file under `## References` and pulls
it in at the end with `{{< include DETAILS.md >}}`, so one page renders
whole and the short form stays readable on its own.

`decisions/` (MADR, `YYYYMMDD-title.md`) still records a single point
decision. `rfd/` records a longer-lived design that can carry a
proposal forward and get amended over time. The project migrates
existing MADR files into `rfd/` gradually. Once a MADR file has a
matching `rfd/NNNN` folder, delete the MADR file. Do not keep a
pointer stub. Git history still holds the deleted file's content and
its old path.

A new RFD takes the next unused four-digit number under `rfd/`; check
`pages/rfd.html`'s live listing (sorted newest first), not any other repo's
own numbering, for what is already taken.

## References

- RFD style: `weftspun/request-for-discussion`, `0000-conventions`
- STE spec: https://www.asd-ste100.org/
- STE linter: the `simplified-technical-english` Claude Code plugin

## Related

See `pages/rfd.qmd` (rendered as `pages/rfd.html`) for the live, sortable index.
