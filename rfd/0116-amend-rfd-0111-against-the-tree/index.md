---
title: "RFD 0116: Amend RFD 0111 against the tree"
rfd: "0116"
state: discussion
scope: architecture vocabulary across all repositories
---

## Problem

RFD 0111 is executed. The thirty renames landed, and GitHub redirects each old
name. Four of its statements disagree with the organisation and the checkout as
they are today. Each statement is the kind a reader takes as a survey of what is
there, so a wrong one sends the next person to a directory or a name that does
not exist. RFD 0111 states its own rule for this case: one source of truth per
fact, and the tree is that source.

## Decision

Amend RFD 0111 in four places. Each amendment below states what the tree holds
on 2026-08-16 and what the text must say instead.

The `fabric-` prefix survives in five live names. RFD 0111 says the word is in
one name after the pass. Fifteen names in the organisation carry the prefix.
Nine of those are archived or are forks that carry an upstream name, which the
convention does not reach. Six are live and owned, and RFD 0111 accounts for one
of them, `fabric-harness`. Amend the sentence to claim the five that remain, and
name them: `fabric-game-observability`, `fabric-godot-assembly`,
`fabric-quickstart`, `fabric-stage-runtime`, and `fabric-wt-harness`.

`entities-godot` states a type that is not its own. The repository is the Godot
engine: `SConstruct`, `editor/`, `drivers/`, `platform/`, `servers/`, and
`thirdparty/`, 1.6 GB of C++. An engine holds no set of entities in the Netflix
sense, so `entities-` asserts a false type. That is the objection RFD 0111 itself
raises to reject `service-meta` and to reject `interactor-anything` for
`contract-command`. Move `entities-godot` into "The names the shape does not
decide" and decide it there on the same ground as the other six.

The retirement of `core` reaches a directory the RFD keeps. RFD 0111 renames
`ports/` to `repositories/` in `loot`, `combat`, and `progression`. The word
`repository` is the one collision RFD 0111 creates, and its resolution is to
write "git repository" in full and keep the bare word for the interface. A
directory named `repositories/` inside a git repository puts that collision in
the tree, where RFD 0111 says a collision costs most. Rename `ports/` to
`repository/`, singular, which reads as the interface and never as a list of
checkouts.

The gap RFD 0111 found is smaller than it states. RFD 0111 says the `lean-*-core`
READMEs describe a layout that no git repository has, and that each holds one Lean
namespace directory. `entities-lean-rebac` holds `Rebac/core/` and `Rebac/ports/`,
with Lean sources in both, so its README is correct and only its paths sit one
namespace deep. `entities-lean-loot` holds `r128gpu/`, `r128test/`, and `parity/`
beside `LootCore/`. Amend the section to correct three READMEs rather than five,
and to state that `entities-lean-rebac` needs its paths qualified rather than
replaced.

RFD 0111's rename list, its conversion table, and its retirement of the deployment
words stand. This RFD changes none of them.

## References

- RFD 0111, amended by this RFD. `rfd/0111-convert-the-deployment-words/`
- RFD 0028, for the `core/`, `ports/`, `adapters/` triad this RFD keeps naming
- RFD 0000, for the rule that one fact has one source and the source is not prose
- The survey, the commands that produced it, and the counts: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
