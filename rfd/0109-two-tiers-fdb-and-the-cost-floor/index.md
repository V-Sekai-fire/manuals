---
title: "RFD 0109: Two tiers, FoundationDB, and 276.48 USD per month as the cost floor"
rfd: "0109"
state: published
scope: tier count, store selection, deployment cost baseline
---

## Problem

`rfd/0107` describes four runtimes: h2o, Janet, a C core, and Godot.
`rfd/0108` adds local C ABI guests to that host. One person cannot
carry four runtimes, and neither record is built.

The tier count moved three times in one day, and the store moved five
times, with no record of either. `rfd/0104` states why little of it
mattered. The database is not the constraint, and bandwidth is, by
roughly 100 times.

No record names the cost of the target. Without a cost floor, every
architecture argument runs on an unstated budget, and each session
re-derives a different answer.

## Decision

**The cost floor is 276.48 USD per month.** That is 1000 concurrent
players at 4 hours per day, from `rfd/0104`. It is table stakes, not a
ceiling. The design assumes it.

**Two tiers.**

- Zone client: Godot. Rendering, XR, IK, and local physics.
- Server: Elixir and Phoenix. Identity, room directory, and the
  presence relay.

The server relays presence rather than simulating it. Phoenix supplies
identity, sessions, and migrations, which a Godot server would need
written in GDScript.

**The store is FoundationDB**, through `ecto_foundationdb`. `rfd/0075`
stands, and it is Apache 2.0, C++, write-optimized, and linearly
scalable by process. `rfd/0103`'s limits are accepted, so no joins, no
`or`, and no aggregates in the database.

That trade holds because the relational need is analytical, and the
analytical half does not use this store. Event logs and measurements
stay zstd Parquet in essential tuple normal form, read by DuckDB.
OLTP access is point lookups by player and room identity.

**taskweft stays an Elixir NIF.** `V-Sekai-fire/multiplayer-fabric-taskweft`
already has that shape. Janet and the C `libtaskweft` are dropped.

This supersedes `rfd/0107` and `rfd/0108`.

## References

- The arithmetic, the stores considered, and the open questions:
  `DETAILS.md`
- `rfd/0104-hypothesis-1000-concurrent`, `rfd/0075-fdb-over-cockroachdb-for-zone-state`

## Related

- `rfd/0103-uro-on-ecto-foundationdb`: the adapter and its limits.
- `rfd/0046-server-authoritative-simulation-deferred-rollback`: the
  authority model a relay does not provide.

## Detail

{{< include DETAILS.md >}}
