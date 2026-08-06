---
title: Replace FabricZone (Godot) with zone-server-h2o (libh2o + FDB + Fil-C)
date: 2026-08-06
status: accepted
decision-makers: K. S. Ernest (iFire) Lee
tier: proof of concept
---

## Context

The production zone server (`zone-server`, deployed as `multiplayer-fabric-zone`
on Fly.io) is a boot scaffold today — OpenTelemetry init only, no WebTransport
listener, no game logic (`project/main.gd`'s own `TODO(cycle-5)` comment). The
real entity/simulation engine, `FabricZone`/`FabricZoneJournal`/`FabricMMOGZone`,
exists as a working Godot C++ module in `V-Sekai-fire/multiplayer-fabric-build`
(`godot/modules/multiplayer_fabric/`) but has never been wired into a deployed
zone server. Separately, `weftspun/h2o-bench-tpcc` designed (RFD 0002,
`discussion` state, never implemented) a `libh2o` + FoundationDB "zonefabric"
scenario modeling the same hub/instanced-zone shape — entity authority via a
Hilbert-curve partition, ghost/AOI interest management — independently of this
org's actual zone-server work.

## Decision

Build [`zone-server-h2o`](https://github.com/v-sekai-multiplayer-fabric/zone-server-h2o):
a native `libh2o` + FoundationDB zone server, built with
[Fil-C](https://github.com/pizlonator/fil-c) for memory safety against
untrusted client input, that fully replaces the Godot `FabricZone` engine on
the **server** side. The client stays Godot engine, unchanged.

Scope carried over from `FabricZone`/`FabricZoneJournal` (not a blank-slate
design): entity slots, zone-to-zone entity migration, ghost/AOI state, and a
durable journal (spawn/despawn/payload-update/snapshot/replay) — reimplemented
against FDB instead of local SQLite, so it is shared across zone-server
processes instead of single-node.

Physics/IK is ported from [`sinew-mocap/solve`](https://github.com/sinew-mocap/solve)
(FK + LBS skinning), constrained by the `lean-humanoid-rom` and
`swing-twist-kusudama` proofs — no working IK implementation existed inside
`FabricZone` itself to port from directly.

Entity and ReBAC types are generated from `lean-entity-packet` and
`lean-rebac-core` respectively, rather than hand-duplicated across the C++
engine being retired, the new FDB/Fil-C code, and any client-facing schema.

First working milestone: a WebTransport datagram round-trip plus a bare
`ZoneTick` (`position += velocity * dt`, no physics) — everything else
(migration, ghosts, physics/IK, Fil-C hardening) is built after that is
proven, not deferred in scope.

`weftspun/h2o-bench-tpcc` is archived once its reusable infrastructure and
zonefabric design are ported. Its accepted TPC-C benchmark work
(`RFD 0001`) is unaffected by this decision and stays there, read-only.

## Consequences

- The Godot zone-server deployment (`zone-server` repo, Fly app
  `multiplayer-fabric-zone`) is retired once `zone-server-h2o` passes
  equivalent verification, in favor of the new implementation.
- `zone-backend` (Uro) is unaffected: it still only does identity, zone
  directory, asset storage, and ReBAC, and still never sees per-entity data
  in the live session.
- CockroachDB's scope stays account-level (identity, zones directory,
  avatars). The one exception under discussion — inventory/profile commits,
  previously headed toward CockroachDB via the progression hexagon's
  SQLite "commit valve" — targets FDB instead, as the single write path for
  everything the zone server owns.
- The related, previously-unimplemented `weftspun/h2o-bench-tpcc` RFDs this
  decision carries forward are filed alongside this entry, dated the same day:
  zonefabric scaling, actor-lite worker pool, FDB selection, verification
  strategy, binary value encoding, async FDB callback chain, zstd
  compression, slotmap entity storage, macaroon/XDP security, feature
  ablation, and the PERT critical path.
