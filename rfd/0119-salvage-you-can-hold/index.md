---
title: "RFD 0119: Salvage you can hold"
rfd: "0119"
state: discussion
scope: client interaction model, authority, the boundary between physics and the ledger
---

## TL;DR

```
gyre X networked physics in vr X pragmata
```

The Gyre supplies an economy a database can prove. Networked physics in VR supplies hands that pass an object between
two people across a network. PRAGMATA supplies the shape of playing both at once.

## Problem

`fabric-store-domain` holds an invariant: salvage is unique, and no item is in two Sparks' hands. A transaction across
two databases enforces it, and `honest()` checks it every cycle.

Glenn Fiedler's VR cubes hold the same invariant under another name. Ownership stops two players holding one cube, and
a sequence number per cube enforces it while a host arbitrates. His rule is exact: "Ownership sequence increments each
time a player grabs a cube. Ownership is stronger than authority, such that an increase in ownership sequence wins
over an increase in authority sequence number."

One invariant, two mechanisms, three orders of magnitude apart in cost. The transaction is exact and takes a round
trip. The sequence number converges and takes nothing.

RFD 0085 makes the question urgent by naming the object that carries it. Memory Drives house a Spark's consciousness,
drop on death, and can be looted or ransomed by other players. A drive is holdable, contested, and the one item in the
setting where duplication is unsurvivable in the fiction as well as in the ledger. Two people holding one drive is two
people holding one person.

## Decision

**Two authorities, split by what a mistake costs.** Physics authority is distributed and taken by whoever last touched
an object, and it is allowed to be briefly wrong. Economic authority stays with the store plane, single-writer and
transactional, and is never allowed to be wrong. A dropped crate costs a frame of jitter. A duplicated drive costs the
invariant every other check rests on.

**The cycle is the line, because a cycle is already one transaction.** `fabric-store-domain` makes each cycle a
single group commit across the ward and every Spark it touches. Salvage loose in the world between cycles is physics
the ledger has never heard of, and the cycle that ends is the commit that takes it. The boundary the interaction model
needs is the boundary the store plane already draws, so nothing new carries it.

**A claim is one transaction that deletes and inserts together.** Converting loose salvage into a row removes the
physical object and writes the `held` entry in the same commit, and drawing an item back into the world runs it
backwards. Uniqueness holds because the ledger counts only what it has committed, and the conversion is the only place
the two representations meet.

**Memory Drives never enter the distributed regime.** Fiedler states his model suits "cooperative experiences only, as
it does not provide the security of a server-authoritative network model". Seven of the Gyre's nine contracts resolve
without a fight, so that limitation costs almost nothing across the setting. Drive looting and ransom is the exception
and is adversarial by design, so custody of a drive stays transactional even while its physical shell is thrown
around.

**Physics never reaches the seeded simulation.** `CLAUDE.md` requires that a cycle not advance on wall-clock time and
that the RNG draw order never move. PhysX is non-deterministic, which is why Fiedler rejected lockstep. A thrown crate
may not decide a contract, feed a draw, or advance a cycle. The physics layer reads the ward and the ward declines to
read it back.

**The board is the second layer, played at the same time.** PRAGMATA runs Hugh's movement and Diana's hacking
together, one player coordinating both. The Gyre has both halves already: hands in the world at frame rate, and the
Queen's board of contracts and cycles as a discrete layer deciding what the object in your hand is worth. Neither
pauses for the other.

## Consequences

The 100-byte entity packet and the interest filter in `fabric-fanout-edge` become the physics transport, which is what
they were built for. `fabric-authority-plane`'s single writer keeps the ledger and holds no opinion about where a
crate is.

Two representations of one object exist while it is loose, and exactly one exists once it is claimed. A bug in the
conversion surfaces as a violated invariant on the next cycle rather than as a visual glitch, which is the failure
mode to want.

The second layer runs against the board the Queen already plays, so it costs content rather than architecture.

## Open questions

Whether the host-arbiter topology survives a dedicated ward process. Fiedler's host is a player; `queen serve` is not,
and it already terminates WebTransport in its own process.

What a claim costs in latency, given it is a parallel commit across two databases while the player is holding the
object.

Whether a drive's physical shell can be thrown at all while its custody stays transactional, or whether the shell has
to be inert to keep the two from disagreeing.

## References

- [Networked Physics in Virtual Reality](https://gafferongames.com/post/networked_physics_in_virtual_reality/), Glenn
  Fiedler: the authority model, the priority accumulator, and the delta encoding
- [PRAGMATA](https://store.steampowered.com/app/3357650/PRAGMATA/), CAPCOM: two characters played at once
- `rfd/0085-the-gyre-mud-setting-on-the-loot-action-shell`: the setting, the Hub and Field loop, and Memory Drives
- `v-sekai-multiplayer-fabric/fabric-store-domain`: the ward, the invariants, and the parallel commit
- `v-sekai-multiplayer-fabric/fabric-fanout-edge`: the interest filter and the entity packet
- `v-sekai-multiplayer-fabric/fabric-authority-plane`: the single writer the ledger keeps

## Detail

{{< include DETAILS.md >}}
