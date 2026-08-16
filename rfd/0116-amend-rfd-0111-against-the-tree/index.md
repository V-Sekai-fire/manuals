---
title: "RFD 0116: Amend RFD 0111 against the tree"
rfd: "0116"
state: discussion
scope: architecture vocabulary across all repositories
---

## Problem

RFD 0111 is executed: the thirty renames landed, and GitHub redirects each old
name. Four of its statements disagree with the organisation and the checkout
today, and each reads as a survey, so a wrong one names a thing that is not there.

## Decision

Amend RFD 0111 in four places. `DETAILS.md` holds the evidence for each, with the
command that produces it and the date it was run.

| the statement                            | the tree on 2026-08-16                                                     | the amendment                                    |
| ---------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------ |
| the word `fabric` is in one name         | fifteen names carry the prefix, six are live and owned, and 0111 names one | claim the five that remain, and list them        |
| `entities-godot` holds entities          | the Godot engine: `SConstruct`, `editor/`, `drivers/`, `servers/`          | move it to the names the shape does not decide   |
| `ports/` becomes `repositories/`         | `repository` is the one collision RFD 0111 creates                         | rename to `repository/`, singular                |
| five READMEs describe absent directories | `entities-lean-rebac` holds `Rebac/core/` and `Rebac/ports/`, both in Lean | correct three READMEs, and qualify rebac's paths |

A fifth claim was checked and withdrawn: repositories named `loot`, `combat`, and
`progression` do hold the RFD 0028 triad, so that statement stands.

The conversion table, the retired deployment words, the type-first name shape, the
thirty renames, and the case for "interactor" all hold, unchanged by this RFD.

## References

- RFD 0111, amended by this RFD. RFD 0028, for the triad this RFD keeps naming
- RFD 0000, for the rule that one fact has one source, and that it is not prose
- The survey, the commands that produced it, and the counts: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
