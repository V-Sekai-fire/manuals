# manuals

Architecture decisions, changelogs, and reference documentation for the v-sekai-multiplayer-fabric stack. Published as a Quarto website.

## Build

```sh
uv sync           # install Python deps
quarto render     # build to _site/
quarto preview    # local preview
```

## Adding a decision

Decisions go in `rfd/`, one folder per record, as `rfd/NNNN-kebab-title/index.md`.
See `rfd/0000-conventions/` for the format, the states, and the `index.md` and
`DETAILS.md` split.

The `decisions/` directory held MADR records before the migration into `rfd/`.
The migration is complete, and what stays there is `madr-proposal-template.md`,
which RFD 0106 keeps as the live template. Git history holds the migrated records
and their old paths, so a link to `decisions/YYYYMMDD-*.md` in an older changelog
entry or RFD points at history rather than at a live file.

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

Commit images beside the RFD that cites them, in `rfd/NNNN-kebab-title/`, using the
archival naming convention `YYYYMMDD_project_description_NNNN.ext` (lowercase, no
spaces, ISO date, zero-padded sequence), and add a matching entry under `references:`
in `CITATION.cff`. See `rfd/0013-archival-file-naming-convention/`.

## Key files

| Path                                 | Purpose                                                           |
| ------------------------------------ | ----------------------------------------------------------------- |
| `_quarto.yml`                        | Site config                                                       |
| `index.md`                           | Landing page                                                      |
| `rfd/`                               | Request-for-Discussion records, one folder each                   |
| `data/measurements/`                 | Quantitative record behind the RFDs, Parquet, off the site        |
| `changelog/`                         | Changelog entries by year                                         |
| `pages/`                             | Site listing pages (`changelog.qmd`, `rfd.qmd`, `references.qmd`) |
| `pages/changelog.qmd`                | Changelog index                                                   |
| `scripts/`                           | Repo tooling: changelog generator, tropes check, Quarto filter    |
| `scripts/create_changelog_entry.exs` | Generate new changelog entry                                      |

## Conventions

- RFD folders: `rfd/NNNN-kebab-title/`, with `index.md` and an optional `DETAILS.md`
- Changelog filenames: `YYYYMMDD-deck-log.md` inside `changelog/YYYY/`
- Asset filenames: `YYYYMMDD_project_description_NNNN.ext` beside the citing RFD, with a `CITATION.cff` entry
- Prose follows tropes.fyi style by hand; `prek run --all-files` must pass before pushing
- No hardcoded absolute filesystem paths; use env vars or placeholders (e.g. `$GODOT_SRC`)
- Do not commit `_site/` — it is build output
- Commit style: sentence case, no `type(scope):` prefix
- One concern per PR; PRs land through a pull request with `prek` green
