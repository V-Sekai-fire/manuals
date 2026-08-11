# manuals

Architecture decisions, changelogs, and reference documentation for the v-sekai-multiplayer-fabric stack. Published as a Quarto website.

## Build

```sh
uv sync           # install Python deps
quarto render     # build to _site/
quarto preview    # local preview
```

## Adding a decision

Create a Markdown file in `decisions/` named `YYYYMMDD-short-title.md` following the
[MADR](https://adr.github.io/madr/) template:

```markdown
---
title: Short title representative of the problem and solution
date: YYYY-MM-DD
status: proposed | accepted | rejected | deprecated | superseded by YYYYMMDD-...
---

## Context and Problem Statement

## Decision Drivers

## Considered Options

## Decision Outcome

Chosen option: "...", because ...

### Consequences

### Confirmation
```

Optional MADR sections (`Pros and Cons of the Options`, `More Information`) may follow.
To supersede an earlier decision, set the old file's `status` to `superseded by <new filename>`
and link back from the new one.

A decision that records a product feature also carries a `tier` in its frontmatter —
`proof of concept`, `baseline`, or `stretch` — per the feature classification decision.
Process and infrastructure decisions carry no tier. The decisions index shows the
`tier` and `status` columns.

## Adding a changelog entry

```sh
elixir scripts/create_changelog_entry.exs        # uses today's date
elixir scripts/create_changelog_entry.exs 20260512
```

## Checks

Pull requests run `prek` (prettier on Markdown), which must pass on a branch that is
up to date with `main` before the PR merges. Run it locally before pushing:

```sh
prek run --all-files          # prettier
```

Prose still follows [tropes.fyi](https://tropes.fyi/) style — no negative parallelism
(`not X, but/it's Y`), no bold lead-in list items (`- **Term:** ...`) — but it is no
longer enforced by CI. `scripts/check_tropes.sh` remains in the repo and can be run by
hand:

```sh
bash scripts/check_tropes.sh
```

## Assets

Commit images under `decisions/attachments/` using the archival naming convention
`YYYYMMDD_project_description_NNNN.ext` (lowercase, no spaces, ISO date, zero-padded
sequence), and add a matching entry under `references:` in `CITATION.cff`. See the
naming-convention decision.

## Key files

| Path                                 | Purpose                                                           |
| ------------------------------------ | ----------------------------------------------------------------- |
| `_quarto.yml`                        | Site config                                                       |
| `index.md`                           | Landing page                                                      |
| `decisions/`                         | Architecture Decision Records not yet migrated to an RFD          |
| `changelog/`                         | Changelog entries by year                                         |
| `pages/`                             | Site listing pages (`changelog.qmd`, `rfd.qmd`, `references.qmd`) |
| `pages/changelog.qmd`                | Changelog index                                                   |
| `scripts/`                           | Repo tooling: changelog generator, tropes check, Quarto filter    |
| `scripts/create_changelog_entry.exs` | Generate new changelog entry                                      |

## Conventions

- Decision filenames: `YYYYMMDD-kebab-title.md`
- Feature decisions carry a `tier:` (`proof of concept` / `baseline` / `stretch`)
- Changelog filenames: `YYYYMMDD-deck-log.md` inside `changelog/YYYY/`
- Asset filenames: `YYYYMMDD_project_description_NNNN.ext` in `decisions/attachments/`, with a `CITATION.cff` entry
- Prose follows tropes.fyi style by hand; `prek run --all-files` must pass before pushing
- No hardcoded absolute filesystem paths; use env vars or placeholders (e.g. `$GODOT_SRC`)
- Do not commit `_site/` — it is build output
- Commit style: sentence case, no `type(scope):` prefix
- One concern per PR; PRs land through a pull request with `prek` green
