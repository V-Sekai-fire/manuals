---
title: "RFD 0021: Require pull requests and a merge queue on main"
rfd: "0021"
state: published
scope: repo branch protection and CI gating
---

## Decision

`main` had no branch protection: pushes landed directly, and
concurrent pull requests validated against an older tip could
conflict once both landed. The repository now applies a ruleset on
the default branch that blocks direct pushes and branch deletion,
requires a pull request (with zero mandatory approvals), and requires
a merge queue that serializes entries against the branch tip before
they land. Two later amendments close gaps found in practice: the
repository enables automatic deletion of a merged pull request's
source branch, since the merge queue itself cannot delete it; and the
ruleset must carry a `required_status_checks` rule naming the real CI
jobs, since the merge-queue rule alone does not require any check to
pass.

## References

- Full context, decision drivers, considered options, consequences,
  confirmation steps, and both amendments: `DETAILS.md`
- Original record:
  `decisions/20260606-require-pr-and-merge-queue-on-main.md`
- `gh api repos/v-sekai-multiplayer-fabric/manuals/rulesets` (ruleset
  id `17352485`)

## Related

- `rfd/0012-amend-pr-before-it-enters-the-queue`
