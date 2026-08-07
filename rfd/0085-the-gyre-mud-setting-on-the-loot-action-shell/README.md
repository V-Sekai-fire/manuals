---
title: "RFD 0085: The Gyre — a MUD setting on the loot-action core-loop shell"
rfd: "0085"
state: discussion
scope: zone-server-h2o game content, web client
---

The premise:

Players awaken as "Sparks" — digitized human consciousnesses legally owned by a defunct hyper-corporation. They are currently downloaded into "Frames," which are cheap, mass-produced synthetic worker chassis. Abandoned on The Gyre, a massive, slowly failing ring-station orbiting a toxic gas giant, players must survive cycle by cycle. They take on grueling localized contracts, scavenge for parts to prevent their Frames from seizing up, and try to buy their digital freedom from the station's automated debt-collection algorithms.

## Decision

The Gyre is game content. It is not a new game architecture.

RFD 0045 defines a loop with two areas: a Hub area and a Field area.
Players start in the Hub area. They travel to a Field area to do one
task. Then they return to the Hub area. The Gyre reuses this same
loop.

In The Gyre, two Hub locations stand in for the Hub area: the
Under-Market and the Commons. Each contract stands in for a Field
task. A contract is one of these: a scavenge run, a hack run, an
exploration run, or (sometimes) a short combat run.

RFD 0045 also defines five core systems: Budgeter, Combat, Loot,
Presence, and Progression. These five core systems stay as they are.
The Gyre adds new content on top of them: rooms, non-player characters
(NPCs), items, and a story frame called the Debt Clock.

Party shape and tone: players explore more than they fight. Combat
happens less often than in a typical Dungeons & Dragons session. A
party has 2 to 4 players. The RFD calls each player a Spark. If a
party has fewer than 4 players, NPC companions can fill the empty
spots. See "Party composition and tone" in `DETAILS.md` for more
detail.

Target client: the target client is a website, not the current
SteamVR build. Players log in with GitHub OAuth. GitHub OAuth carries
each player's save data between sessions. This design needs one new
part: a save-data adapter for the Progression core. It does not need
changes to the Combat core, the Loot core, or the Budgeter core. This
RFD does not yet decide the OAuth design or the website design.

Implementation status: `zone-server-h2o` pull request #5 builds the
smallest part of this loop as real code. It adds a `the_gyre` MUD
domain. (A MUD is a multi-user, text-based game.) It also adds a mode
selector on the website. See "Smallest-loop implementation status" in
`DETAILS.md` for which parts are complete and which parts are not
complete. This RFD is the source of truth for the design, not
`zone-server-h2o` issue #4 (closed).

## References

- Room graph, NPCs, contract catalog, item table, session pacing,
  party/tone detail, implementation status, and open questions:
  `DETAILS.md`
- Implementation: `zone-server-h2o` PR #5

## Related

- `rfd/0045-loot-action-core-loop-mvp-vertical-slice`: defines the
  Hub/Field loop and the five core systems that The Gyre reuses.
- `rfd/0028-hexagonal-core-ports-adapters`,
  `rfd/0043-hexagon-progression-core`: describe the shape a future
  web/OAuth save adapter would follow.
