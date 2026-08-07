---
title: "RFD 0059: Status reports lead with the bottom line"
state: published
scope: prose voice for status reports (BLUF convention)
---

## Decision

A status report in this project states the outcome first: the slip,
the failure, or the result, in the opening sentence, with no warm-up
and no apology. The explanation follows, and it gives the factual
reason. The report closes with the next step. This order applies to a
good outcome as well as a bad one; only the order stays fixed. The
report does not open with a progress buffer that saves the outcome for
the end. A reader who reads only the first line already knows where
the work stands; the rest of the report serves a reader who wants the
why and the next step. This rule stays mechanical, so a reviewer can
check it without debate: does the first sentence state the outcome, or
does it delay it?

## References

- Full drivers, considered options, consequences, and confirmation:
  `DETAILS.md`
- Original record:
  `decisions/20260613-bad-news-reports-lead-with-the-bottom-line.md`

## Related

- `rfd/0025-tenseless-continuous-present-voice`: the companion voice
  rule for prose across the repo.
