---
title: "RFD 0120: The Gyre became a settlement game"
rfd: "0120"
state: discussion
scope: the Gyre's shape, the player's role, and what the ward simulates
---

## Problem

RFD 0085 records the Gyre as a MUD on the loot and action shell: a Hub in the Under-Market and the Commons, bounded
contracts out in the field, six zones, and a player who is a Spark taking work to pay down a debt.

`fabric-store-domain` built something else. The player is the Queen, the Sparks act on their own, and the loop is
commissioning rather than travelling. The code has run this way since the first ward played, and the record still
describes the earlier design. Anyone reading 0085 to understand what `queen` does will be wrong about the player, the
loop, and the map.

This RFD records what was built, so the two stop disagreeing.

## Decision

**The player is the Queen, and the Queen never takes a contract.** The shape is `My Life as a King`: commission, then
wait. Sparks choose their own work, and the whole of the player's game is deciding what to build and in what order.
The comment in `src/queen.c` states the reasoning, which is that a loop like this is a state machine over days with
nothing in the critical path to draw, and that is the one game shape genuinely better as a database than as an engine.

**Six venues replace six zones.** The Under-Market and the Commons survive as the two decks a venue stands on, thirty
metres apart. What they hold is a build list rather than a map to travel: Cycle's End Tavern, Splicer's Den, Transit
Rails, Exchange Plaza, Chapel of the Backup, Broadcast Row. Each changes how Sparks behave rather than granting a
number, so the Tavern makes them bolder because they rest and the Rails put more work on the board.

**A contract resolves against risk, on the board, in a cycle.** Nine kinds post to a board of six, or nine once the
Rails stand. A Spark takes one if its nerve carries it, and a draw against the contract's risk decides the outcome.
Seven of the nine still resolve without a fight, which is the part of 0085 that carried over unchanged.

**The Debt Clock is the antagonist, and it compounds.** Debt grows one percent per cycle and the treasury pays it
down. Income from contracts is the only thing that makes scrip, which is what lets one sum decide whether the ward is
honest.

**The currency is scrip.** 0085 calls it chits. The implementation calls it scrip throughout, and the invariant is
written in those terms.

**A cycle is game time and never wall-clock time.** The ward publishes at 20 Hz because the rest of the fabric does,
and that clock says nothing except how often the ward publishes. Tying the two would tie the rate debt compounds at to
the rate the network publishes at, and it would end the replay check.

## What has not been built

The Reclamation Wards, the Tangle, the Sub-Net and the Underhull have no representation in the ward. Splicer Jax,
Overseer Q-11 and Rook are absent, though the Splicer's Den carries Jax's role as a venue. Memory Drives, and the
looting and ransoming of them, are unimplemented, which matters because they are the setting's one adversarial
interaction and RFD 0119 turns on them.

These stay in 0085 as setting. This RFD narrows what `fabric-store-domain` claims to simulate rather than retiring
the fiction around it.

## Consequences

0085 remains the setting record and stops being the design record for the ward. A reader who wants to know what the
simulation does reads this one.

The salvage and interaction model in RFD 0119 sits on the cycle boundary rather than on a Hub and Field loop, because
the loop it was written against is not the loop that exists.

## References

- `rfd/0085-the-gyre-mud-setting-on-the-loot-action-shell`: the setting, which this amends rather than replaces
- `v-sekai-multiplayer-fabric/fabric-store-domain`: `src/queen.c`, the venues, the board, and the clock
- `rfd/0119-salvage-you-can-hold`: the interaction model that depends on which loop is real

## Detail

{{< include DETAILS.md >}}
