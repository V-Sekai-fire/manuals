---
title: "RFD 0011: Replace Jaeger with VictoriaTraces for trace storage"
rfd: "0011"
state: published
scope: observability
---

## Problem

The single-machine observability stack ran Jaeger all-in-one for trace
storage. Jaeger's Badger backend carries a single-node limit. Jaeger
also put traces under a separate vendor from the stack's metrics and
logs backends. Its ports and CLI flags did not match the conventions
the rest of the stack already used.

## Decision

The single-machine observability stack replaces Jaeger all-in-one with
VictoriaTraces, an Apache 2.0 trace backend that accepts OTLP directly.
VictoriaMetrics benchmarks report 3.7 times less RAM and 2.6 times less
CPU than Tempo. This choice puts all three storage backends — metrics,
logs, and traces — under one vendor, drops Badger's single-node limit,
and matches the port and CLI-flag conventions the stack already uses.
Jaeger is removed entirely; no separate query UI process remains.

VictoriaTraces listens on port 10428 for its UI, its query API, and OTLP
HTTP ingest. The OTEL Collector exports traces to it through
`otlphttp/traces`. Data persists at `/var/lib/victoriatraces`.

Note: the stack has since moved off Fly.io onto the Harvester cluster;
the Fly-specific details below predate that move.

## References

- Port map, deployment path, and consequences: `DETAILS.md`
- Original record: `decisions/20260506-observability-stack-victoriatraces.md`
- Supersedes: `decisions/20260506-observability-stack-victoriametrics-jaeger.md`

## Detail

{{< include DETAILS.md >}}
