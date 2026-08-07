---
title: "RFD 0085: The Gyre — a MUD setting on the loot-action core-loop shell"
rfd: "0085"
state: discussion
scope: zone-server-h2o game content, web client
---

## Decision

The Gyre is content, not a new architecture. It reskins the existing
Hub-to-Field-to-Hub loop from `rfd/0045`: the Under-Market and the
Commons stand in for the Hub, and each contract (mostly a scavenge, a
hack, or an exploration run, occasionally a short combat) is a Field
instance. The five hexagonal cores stay the systems of record; The
Gyre supplies rooms, NPCs, items, and a Debt Clock framing.

Target tone and party shape: exploration-forward, fewer combat
encounters per session than a typical D&D-paced game, a party of 2-4
Sparks, and recruitable NPC companions filling out a party below 4
humans. See "Party composition and tone" in `DETAILS.md`.

The target client is a website, not the current SteamVR build, with
GitHub OAuth login carrying save data. That needs a new Progression
persistence adapter, not a change to the Combat, Loot, or Budgeter
cores. This RFD does not commit to the OAuth/web design yet.

`zone-server-h2o` PR #5 lands the smallest slice of this loop as real
code: a `the_gyre` MUD domain and a website mode selector. See
"Smallest-loop implementation status" in `DETAILS.md` for what is
verified and what is not. This RFD, not `zone-server-h2o` issue #4
(closed), is the design's source of truth.

## References

- Room graph, NPCs, contract catalog, item table, session pacing,
  party/tone detail, implementation status, and open questions:
  `DETAILS.md`
- Implementation: `zone-server-h2o` PR #5

## Related

- `rfd/0045-loot-action-core-loop-mvp-vertical-slice`: the Hub/Field
  loop and the five cores this content reuses.
- `rfd/0028-hexagonal-core-ports-adapters`, `rfd/0043-hexagon-progression-core`:
  the shape a web/OAuth save adapter would follow.
