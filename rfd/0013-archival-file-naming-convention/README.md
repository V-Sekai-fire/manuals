---
title: "RFD 0013: Archival file naming convention for committed assets"
rfd: "0013"
state: published
scope: decisions/attachments
---

## Decision

Committed binary assets (screenshots and similar files under
`decisions/attachments/`) follow a Library of Congress style descriptive
naming pattern:

```
YYYYMMDD_project_description_NNNN.ext
```

The pattern uses lowercase ASCII only, an ISO 8601 date first so names
sort chronologically, underscores between facets, hyphens within a
facet, and a zero-padded sequence number so same-day captures stay
unique and ordered. This convention was chosen over keeping source names
or using content-hash names, because it follows recognized digital
preservation guidance and produces names that sort and explain
themselves.

Example: `20260606_vsekai-mpf_xr-grid-debug-orbs_0001.png`.

Each committed asset also gets a BibTeX entry in `references.bib`
recording its capture date and archived path.

## References

- Decision drivers, considered options, and confirmation: `DETAILS.md`
- Original record: `decisions/20260606-archival-file-naming-convention.md`
