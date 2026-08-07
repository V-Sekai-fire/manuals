---
title: "RFD 0103: PostgreSQL with WAL to S3 for Uro, and DuckDB only for analytics"
rfd: "0103"
state: discussion
scope: zone-backend, aria-storage
---

## Problem

`rfd/0006` puts Uro on CockroachDB with mTLS role separation. That
predates the 15 USD Fly budget in `rfd/0102`.

CockroachDB Cloud Basic is on the blocklist. Self-hosting costs RAM at
about 5 USD per GB per month on Fly, and CockroachDB wants gigabytes.

The requirement is to keep Ecto and Postgrex, and to checkpoint to S3.

## Data

Every figure below is measured in a 256 MB container, or taken from a
published price.

| Option                                  | Fixed USD | Concurrent at 4 h/day | Keeps Ecto       |
| --------------------------------------- | --------- | --------------------- | ---------------- |
| DuckDB embedded in Uro                  | 4.19      | 39.1                  | no, rewrite      |
| FRL, server colocated at 512 MB         | 5.49      | 34.4                  | yes, new adapter |
| **PostgreSQL colocated, Uro at 512 MB** | **5.64**  | **33.9**              | **yes**          |
| PostgreSQL on its own 256 MB machine    | 6.36      | 31.2                  | yes              |
| FRL, server on its own 512 MB machine   | 7.51      | 27.1                  | yes, new adapter |
| FRL, server on its own 1 GB machine     | 10.11     | 17.7                  | yes, new adapter |
| Self-hosted CockroachDB, 1 GB           | 10.26     | 17.1                  | yes              |
| Neon, paid, always on at 1 CU           | 81.59     | over budget           | yes              |

The colocated FRL row is MEASURED. See below.

Point-read latency, both measured in 256 MB:

| Engine        | Point SELECT |
| ------------- | ------------ |
| PostgreSQL 16 | **0.084 ms** |
| DuckDB        | 0.919 ms     |

PostgreSQL is approximately 11 times faster at point reads, in the same
memory, and it needs no change to Uro's data layer.

## Decision

Uro runs on **PostgreSQL**, self-hosted on Fly, with WAL archived to
Tigris for point-in-time recovery.

DuckDB stays, and only for analytics and telemetry, writing ETNF
Parquet. That is the workload it is good at, and `lean-duckdb` already
writes that format here.

## Why not Neon

Neon's free plan forces scale-to-zero. The database suspends after 5
minutes of inactivity, and the plan cannot be kept always on.

A game backend cannot accept a cold start on the first login after an
idle period. The free plan also gives 100 CU-hours per month, which is
4.2 days of always-on running.

Paid compute is 0.106 USD per CU-hour. One CU held for a month is about
77 USD, which is five times the whole budget.

The same reasoning applies to any serverless Postgres that bills by
active compute. Scale-to-zero suits bursty web apps. It does not suit a
service that must answer a login immediately.

## FoundationDB's Relational Layer, and why it is not decided here

`weftspun/ecto-fdb-relational` is an Ecto adapter for FoundationDB
Record Layer's Relational Layer. It speaks gRPC to
`fdb-relational-server`'s JDBCService, with no JDBC, JVM or NIF bridge
on the Elixir side. `weftspun/ecto-bench-tpcc` benchmarks it.

The architectural argument is real and it is the strongest of any
option here. `rfd/0102` already runs FoundationDB on the zone machine.
Using it for Uro removes a second datastore, and the adapter belongs to
this organization.

The memory objection is now measured away.
`fdb-relational-server` 4.3.6.0 from Maven Central, on JDK 21, in a 512
MB container that also ran `fdbserver`:

    RSS 157.0 MB
    Started on grpcPort=1111/httpPort=1112 with services:
      grpc.health.v1.Health, grpc.reflection.v1alpha.ServerReflection,
      grpc.relational.jdbc.v1.JDBCService

157 MB fits beside Uro on one 512 MB machine, at 34.4 concurrent users.
That beats PostgreSQL colocated, which reaches 33.9, and it removes a
datastore rather than adding one.

One gap remains, and it is query latency. PostgreSQL measured 0.084 ms
per point read. There is no equivalent figure for FRL, and neither
repository publishes `ecto-bench-tpcc` results.

FRL's dialect is also "close to but not standard SQL", by its own
README. Uro's migrations need porting either way, and this port targets
a dialect with one implementation.

So FRL leads on cost and on architecture, and it needs one more
measurement before it takes the decision. Run `ecto-bench-tpcc` against
`fdb-relational-server` and compare point-read latency with 0.084 ms.

## Why not DuckDB for this

DuckDB measured well, and it is the wrong shape for Uro's OLTP.

Point reads are 0.919 ms against PostgreSQL's 0.084 ms. DuckDB permits
one writing process. And moving Uro off Ecto and Postgrex is
unestimated work, spent to reach a slower result.

DuckDB is 1.45 USD per month cheaper, which is 5.2 concurrent users.
That is not worth a data-layer rewrite.

## Why PostgreSQL rather than CockroachDB

CockroachDB earns its cost with distribution and multi-region. Neither
is in `rfd/0102`'s topology, which is one region and one Uro node.

PostgreSQL runs the same wire protocol, so `Ecto.Adapters.Postgres` and
Postgrex are unchanged. Uro's migrations need review for
CockroachDB-specific SQL, and that review is not done.

`rfd/0006`'s mTLS role separation carries over. PostgreSQL supports
client-certificate authentication and per-role privileges, so
`gateway_writer` and `gateway_admin` keep their shape.

## Recovery

WAL archives continuously to Tigris, which charges 0 USD egress. A base
backup plus WAL gives point-in-time recovery.

This matches what `rfd/0100` does for FoundationDB. Live data sits on
the Fly volume, and recovery data sits in the object store.

## Open

FRL's query latency is unmeasured. `fdb-relational-server` fits at 157
MB RSS, so cost no longer decides this. Latency does, and 0.084 ms is
the number to beat.

Uro's migrations are not audited for CockroachDB-specific SQL.

Whether PostgreSQL and Phoenix fit together in 512 MB is unmeasured.
The separate-machine row costs 2.7 concurrent users and removes that
risk.

Uro's real row counts and request rate are unmeasured.

## Sources

- Measurements above, PostgreSQL 16 and DuckDB in 256 MB containers
- [Fly pricing](https://fly.io/docs/about/pricing/), about 5 USD per GB of RAM per month
- [Neon pricing](https://neon.com/pricing), free plan scale-to-zero and 0.106 USD per CU-hour
- [weftspun/ecto-fdb-relational](https://github.com/weftspun/ecto-fdb-relational), the FRL adapter
- [weftspun/ecto-bench-tpcc](https://github.com/weftspun/ecto-bench-tpcc), the benchmark harness
- `rfd/0006`, CockroachDB with mTLS role separation
- `rfd/0102`, the 15 USD deployment budget
