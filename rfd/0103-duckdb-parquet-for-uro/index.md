---
title: "RFD 0103: DuckDB and Parquet for Uro, not CockroachDB"
rfd: "0103"
state: discussion
scope: zone-backend, aria-storage
---

## Problem

`rfd/0006` puts Uro on CockroachDB with mTLS role separation. That
decision predates the 15 USD Fly budget in `rfd/0102`.

CockroachDB Cloud Basic is on the blocklist, so the managed free tier
is not available. Self-hosting on Fly costs RAM at about 5 USD per GB
per month.

| Option                        | Fixed USD | Concurrent at 4 h/day |
| ----------------------------- | --------- | --------------------- |
| Self-hosted CockroachDB, 2 GB | 15.45     | **over budget**       |
| Self-hosted CockroachDB, 1 GB | 10.26     | 17.1                  |
| **DuckDB embedded in Uro**    | **4.19**  | **39.1**              |

A 2 GB node exceeds the entire budget before any bandwidth. A 1 GB node
costs 22 concurrent users, which is more than half of them.

A single-node CockroachDB also failed to start in a 512 MB container in
testing. The cause was not isolated, so treat that as a warning rather
than a limit.

## Decision

Uro stores its data in DuckDB, writing Parquet in essential tuple
normal form, with Parquet snapshots to S3 for recovery.

DuckDB is embedded, so it needs no machine of its own. `lean-duckdb`
already writes ETNF Parquet in this organization, so the format is not
new here.

## Measurements

Run in a 256 MB container with a 128 MB DuckDB memory limit.

| Measure                              | Result    |
| ------------------------------------ | --------- |
| Peak resident memory                 | 103.9 MB  |
| 200000 identity rows as zstd Parquet | 0.32 MB   |
| Scan query over 200000 rows          | 3.5 ms    |
| `read_parquet` count                 | 1.0 ms    |
| Point SELECT                         | 919.1 us  |
| Point UPDATE                         | 1190.4 us |

## Why 919 us per point read is acceptable

It is approximately 1000 times slower than an OLTP engine, and the
workload is far below what that allows.

DuckDB serves roughly 1000 point operations per second on one thread.
Uro at 39 concurrent users, each making about 10 requests per minute,
needs 6.5 requests per second. That is 150 times of headroom.

Identity, the zone directory and the planner are read-mostly and low
rate. Nothing in Uro's workload resembles the high-concurrency,
single-row write pattern that DuckDB is bad at.

## What is given up, stated plainly

**Single writer.** DuckDB permits one writing process. Uro is one BEAM
node today, so this costs nothing now, and it blocks running two Uro
instances against one store.

**No distributed transactions, and no multi-region.** CockroachDB
offers both. If the fabric later needs a second region for Uro itself,
this decision has to be revisited.

**mTLS role separation has no direct equivalent.** `rfd/0006` separates
`gateway_writer` from `gateway_admin` with client certificates. An
embedded file has file permissions instead, which is a weaker boundary
inside one process.

**Migration cost.** Uro uses Ecto and Postgrex against CockroachDB. Its
data layer has to change, and that work is not estimated here.

## Recovery

The DuckDB file lives on the Fly volume. Parquet snapshots go to
Tigris, which charges 0 USD egress.

200000 identity rows compress to 0.32 MB, so a full snapshot is cheap
enough to take often. Recovery reads Parquet back with `read_parquet`,
measured at 1.0 ms for a full count.

This is the same split `rfd/0100` sets for FoundationDB: live data
local, recovery in the object store.

## Open

Uro's real row counts and request rate are unmeasured. The 150 times
headroom above uses an estimate of 10 requests per user per minute.

Whether Ecto can sit on DuckDB, or whether the data layer is replaced
outright, is undecided.

## Sources

- Measurements above, DuckDB 256 MB container probe
- [Fly pricing](https://fly.io/docs/about/pricing/), about 5 USD per GB of RAM per month
- `rfd/0006`, CockroachDB with mTLS role separation
- `rfd/0102`, the 15 USD deployment budget
