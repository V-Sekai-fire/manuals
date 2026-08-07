# Details

## Deployment note

The stack now runs on the Harvester cluster; it has moved off Fly.io
(see self-host on Harvester HCI). The Fly volume and `fly proxy`
references below are from the original deployment.

## Context

Jaeger all-in-one with Badger storage was chosen as the Apache 2.0
replacement for Tempo. VictoriaMetrics ships VictoriaTraces — an Apache
2.0 trace backend that accepts OTLP directly. VictoriaMetrics benchmarks
report 3.7x less RAM and 2.6x less CPU vs Tempo.

Using VictoriaTraces puts all three storage backends (metrics, logs,
traces) under the same vendor, drops Badger's single-node limit, and
matches the port and CLI-flag conventions already in use.

## Port map after this change

| Service         | Port                     | Purpose                          |
| ---------------- | ------------------------ | --------------------------------- |
| VictoriaMetrics  | 8428                     | Metrics storage and PromQL        |
| VictoriaLogs     | 9428                     | Log storage and query             |
| VictoriaTraces   | 10428                    | Trace storage and query           |
| OTEL Collector   | 4317 (gRPC), 4318 (HTTP) | OTLP ingest, routes to the above  |

## Consequences

- All four services are now Apache 2.0; the three storage backends are
  from VictoriaMetrics.
- VictoriaTraces query UI is at `http://...:10428/select/vmui`.
- `fly proxy 10428:10428` replaces the former `fly proxy 16686:16686`
  for trace inspection.
- No explicit trace TTL is configured; add `-retentionPeriod` if disk
  pressure becomes a concern.
