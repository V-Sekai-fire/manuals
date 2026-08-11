---
title: "RFD 0021: Require pull requests on main"
rfd: "0021"
state: published
scope: repo branch protection and CI gating
---

## Problem

`main` had no branch protection. Pushes landed directly on the
branch. Pull requests merged with no guarantee that their checks ran
against the tip they were about to join.

## Decision

The repository applies a ruleset on the default branch that blocks
direct pushes and branch deletion, requires a pull request (with zero
mandatory approvals), and requires the real CI jobs to pass with a
strict up-to-date policy, so a PR rebases onto the current tip before
it merges. The repository also enables automatic deletion of a merged
pull request's source branch, so merged feature branches do not pile
up.

A merge queue is not part of the policy. The strict
`required_status_checks` policy covers the same ground at this volume
of changes, without the enqueue step, the snapshot races, and the rules
the queue needed around branch deletion and late fixes.

## References

- Full context, options, consequences, and confirmation: `DETAILS.md`
- Original record:
  `decisions/20260606-require-pr-and-merge-queue-on-main.md`
- `gh api repos/v-sekai-multiplayer-fabric/multiplayer-fabric-manuals/rulesets` (ruleset
  id `17352485`)

## Detail

{{< include DETAILS.md >}}
