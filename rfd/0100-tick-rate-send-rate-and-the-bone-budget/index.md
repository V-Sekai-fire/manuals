---
title: "RFD 0100: 256 kbps per client, one machine, 47 concurrent"
rfd: "0100"
state: discussion
scope: zone-server-h2o, zone-guest-godot
---

## Decision

**256 kbps per client. One Fly machine. 47 concurrent at peak.**

The budget is 15 USD per month. Bandwidth is the only binding
constraint, so spend the budget on bandwidth and not on machines.

## Topology

    1 Fly machine, shared-cpu-1x, 256 MB, region iad
      |- fdbserver, single process, memory storage
      |- zone-server-h2o, one zone, ZONE_TICK_HZ 64
      |- UDP 7443 bound to fly-global-services -> WebTransport clients
      +- no TCP service: no HTTP surface remains

One process serves one zone. To add zones, add machines and join them
over 6PN, where `<app>.internal` resolves every machine. `rfd/0096`
measured that path at 880 us median between two machines in `iad`.

## Machine cost against concurrency

A `shared-cpu-1x` 256 MB machine is 2.02 USD per month. Egress is 0.02
USD per GB in North America and Europe. At 256 kbps a client uses
0.1152 GB per hour.

| Machines | Machines USD | Egress USD | GB  | Client-hours | 24/7 | 4 h/day peak |
| -------- | ------------ | ---------- | --- | ------------ | ---- | ------------ |
| **1**    | 2.02         | 12.98      | 649 | 5634         | 7.8  | **46.9**     |
| 2        | 4.04         | 10.96      | 548 | 4757         | 6.6  | 39.6         |
| 3        | 6.06         | 8.94       | 447 | 3880         | 5.4  | 32.3         |
| 4        | 8.08         | 6.92       | 346 | 3003         | 4.2  | 25.0         |

Every added machine costs about 7 concurrent users at peak. So run one
machine until a second zone is genuinely needed.

Asia Pacific doubles the egress price, and Africa and India multiply it
by six.

## What binds, and what does not

| Resource                     | At 47 clients         | Ceiling     |
| ---------------------------- | --------------------- | ----------- |
| Egress                       | 649 GB per month      | **binding** |
| CPU, zstd compression        | 3.2 percent of a core | not binding |
| Memory, per-client baselines | 2.1 MB                | not binding |

`rfd/0101` measured compression at 68 us per client per tick. At 10 Hz
that is 0.068 percent of a core per client.

Reuse one `ZSTD_CCtx` across clients rather than holding one each.
Compression runs sequentially inside the tick, and a per-client context
would cost roughly 1.3 MB each, which is 61 MB at 47 clients.

## How 256 kbps is met

    8 avatars, 56 entities each, zstd L3 delta at 10 Hz  = 221.9 kbps
    Opus voice, server-mixed, VOIP mode                  =  24.0 kbps
    total                                                = 245.9 kbps

## Two corrections this depends on

**Three rates, not one.** Simulation stays at `ZONE_TICK_HZ` 64 for the
fixed integer step. State sends at 10 Hz. Voice sends at 50 Hz, from
the 20 ms Opus packets already in `modules/speech`. `rfd/0096` through
`rfd/0099` assumed one rate and produced 10.2 Mbit per second.

**An entity is a bone.** VRM 1.0 gives 55 humanoid bones plus 1 root,
so 56 per avatar, and only the root and hips translate. `rfd/0002`'s
200 entities is 3.6 avatars, not 200 objects.

## Consequences

Interest management is required. 8 avatars fits 256 kbps. 47 does not,
so a client sees 8 of the 47 at full rate.

One machine means one FoundationDB process with memory storage, and a
restart loses zone state. That is the price of spending the budget on
bandwidth. A second machine buys durability and costs 7 concurrent
users.

`modules/speech` sets `OPUS_APPLICATION_AUDIO` and never calls
`OPUS_SET_BITRATE`, so it takes the default near 64 kbps, which is 25
percent of the cap. Set the bitrate, and evaluate
`OPUS_APPLICATION_VOIP`.

Server-side voice mixing is unbuilt. Without it, voice grows with
speaker count and the cap breaks.

## Sources

- Fly pricing, for 0.02 USD per GB and 2.02 USD per machine
- [Networking for Physics Programmers, GDC 2010](https://www.gamedevs.org/uploads/networking-for-physics-programmers.pdf), Sony Bandwidth Probe
- [VRM 1.0 humanoid](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/humanoid.md), 55 bones
- `rfd/0096` for the 6PN measurement, `rfd/0101` for the zstd rate
