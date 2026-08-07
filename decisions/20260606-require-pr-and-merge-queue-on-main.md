---
title: Require pull requests and a merge queue on main
date: 2026-06-06
status: accepted
decision-makers: K. S. Ernest (iFire) Lee
tier: baseline
---

> Moved to [rfd/0021](../rfd/0021-require-pr-and-merge-queue-on-main/README.md).

## Context and Problem Statement

The `manuals` repo had no branch protection on `main`. Changes landed by pushing
directly or by manually merging pull requests one at a time, with no serialization
between concurrent PRs. As the number of in-flight documentation PRs grows, two
PRs can each pass against an older `main` and then conflict or break the Quarto
build once both land. How should changes reach `main` so that every merge is
reviewable and tested against the tip it will actually join?

## Decision Drivers

- Every change to `main` should arrive through a pull request, not a direct push.
- Concurrent PRs should serialize so each is validated against the latest `main`.
- The team is small, so the process should add little ceremony (no mandatory
  second reviewer).
- The setting should be declarative and recorded, not click-ops folklore.

## Considered Options

- Leave `main` unprotected (status quo).
- Branch protection requiring a pull request only.
- A repository ruleset requiring a pull request plus a merge queue.

## Decision Outcome

Chosen option: "A repository ruleset requiring a pull request plus a merge queue",
because it serializes merges and keeps `main` PR-only without forcing a second
reviewer.

The ruleset targets the default branch with these rules:

- Block branch deletion and non-fast-forward pushes.
- Require a pull request, with `0` required approvals (review is allowed, not
  mandated) and all three merge methods permitted on the PR.
- Require a merge queue using the merge commit method, `ALLGREEN` grouping, up to
  5 entries built and merged per batch, and a 1-minute minimum wait.

### Consequences

- Good: `main` only changes through PRs, and the queue tests each entry against
  the branch tip before it lands.
- Good: the configuration is captured here and reproducible from the ruleset JSON.
- Bad: solo edits now need a PR and an enqueue step.
- Bad: with `0` required approvals, the rule enforces process but not review, so
  an unreviewed PR can still merge.

### Confirmation

The ruleset is active (id `17352485`). `gh api repos/v-sekai-multiplayer-fabric/manuals/rulesets`
lists it, and a direct push to `main` is rejected. Future PRs land via the queue.

## More Information

Created with `gh api -X POST repos/v-sekai-multiplayer-fabric/manuals/rulesets`.
To change the policy, edit the ruleset rather than protecting the branch through
the classic branch-protection API, so the two mechanisms do not overlap.

## Amendment (2026-07-12): auto-delete head branches after merge

Force branch deletion after merge by enabling the repository's **automatically
delete head branches** setting (`delete_branch_on_merge`). When a PR merges, its
source branch is removed automatically, so merged feature branches do not pile up.

Why this is a repo setting and not part of the ruleset:

- The merge queue rejects deletion at merge time — `gh pr merge --delete-branch`
  fails with _"Cannot use `-d` or `--delete-branch` when merge queue enabled"_, so
  the per-merge flag cannot do the cleanup. The repo-level `delete_branch_on_merge`
  setting fires after the queue lands the commit and is the correct mechanism.
- It does **not** conflict with the ruleset's _"block branch deletion"_ rule. That
  rule protects the ruleset's target (the default branch) from being deleted; this
  setting deletes the **merged PR's source branch**. Different branches, different
  mechanisms.

Apply it declaratively:

```sh
gh api -X PATCH repos/v-sekai-multiplayer-fabric/<repo> \
  -F delete_branch_on_merge=true
```

### Confirmation

`gh api repos/v-sekai-multiplayer-fabric/<repo> --jq .delete_branch_on_merge`
returns `true`, and the source branch of a merged PR no longer exists.

## Amendment (2026-07-14): the merge queue rule alone does not require CI

The `merge_queue` rule (`grouping_strategy: ALLGREEN`) only controls how the
queue batches and lands entries. On its own it does not name any CI job as a
precondition, so a repo with `pull_request` + `merge_queue` and no separate
`required_status_checks` rule will merge a PR through the queue even if every
check on it failed, or if no check ran at all. This was found on two dependent
repos (`taskweft/taskweft`, `taskweft/nif`) that had the `pull_request` +
`merge_queue` rules from this decision applied without a `required_status_checks`
rule alongside them.

Every ruleset built from this decision needs a `required_status_checks` rule
listing the repo's actual CI job names, added next to the existing
`pull_request` and `merge_queue` rules:

```sh
gh api repos/<org>/<repo>/rulesets/<id> --jq '.rules'
```

lists the current rules; job names to require come from a real PR's checks:

```sh
gh pr checks <PR-number> --repo <org>/<repo>
```

Then `PUT` the full rule array back with a `required_status_checks` entry added
(the API replaces the whole rule list, so read it first and re-add every
existing rule, not just the new one):

```sh
gh api -X PUT repos/<org>/<repo>/rulesets/<id> --input ruleset-with-checks.json
```

where the new rule takes the shape:

```json
{
  "type": "required_status_checks",
  "parameters": {
    "strict_required_status_checks_policy": true,
    "required_status_checks": [{ "context": "<job name from gh pr checks>" }]
  }
}
```

This repo's own ruleset (id `17352485`) already carries a
`required_status_checks` rule for `prek` and `tropes` and was not affected;
the gap was specific to the two repos named above.

### Confirmation

`gh api repos/<org>/<repo>/rulesets/<id> --jq '.rules[] | select(.type == "required_status_checks")'`
returns the rule with the expected job names, and a PR with a failing check
cannot be merged by the queue.
