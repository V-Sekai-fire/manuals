---
title: "RFD 0085: The Gyre — a MUD setting on the loot-action core-loop shell"
state: prediscussion
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

This RFD does not change any code in `zone-server-h2o`; its working
copy is that repo's issue [#4](https://github.com/v-sekai-multiplayer-fabric/zone-server-h2o/issues/4).

## References

- Room graph, NPCs, contract catalog, item table, session pacing,
  party/tone detail, and open questions: `DETAILS.md`
- Source design: `zone-server-h2o` issue #4

## Related

- `rfd/0045-loot-action-core-loop-mvp-vertical-slice`: the Hub/Field
  loop and the five cores this content reuses.
- `rfd/0028-hexagonal-core-ports-adapters`, `rfd/0043-hexagon-progression-core`:
  the shape a web/OAuth save adapter would follow.
