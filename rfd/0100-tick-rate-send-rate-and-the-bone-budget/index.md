---
title: "RFD 0100: The per-client bandwidth cap is 256 kbps"
rfd: "0100"
state: discussion
scope: zone-server-h2o, zone-guest-godot
---

## Decision

**256 kbps per client, downstream.** Cost sets it, not client capacity.

Fly charges 0.02 USD per GB. A `shared-cpu-1x` 256 MB machine is 2.02
USD per month. At 15 USD, two machines leave 10.96 USD, which is 548 GB.

| Per-client rate | Client-hours per month | Concurrent, 24/7 |
| --- | --- | --- |
| 648.6 kbps | 1878 | 2.6 |
| 443.9 kbps | 2743 | 3.8 |
| **256 kbps** | **4757** | **6.5** |

4757 client-hours is 16 concurrent users for 10 hours a day, which is
one social VR instance. Asia Pacific costs twice this, and Africa and
India cost six times.

## How it is met

    8 avatars, 56 entities each, zstd L3 delta at 10 Hz  = 221.9 kbps
    Opus voice, server-mixed, VOIP mode                  =  24.0 kbps
    total                                                = 245.9 kbps

`rfd/0101` measured the compression.

## Two corrections this depends on

**Three rates, not one.** Simulation stays at `ZONE_TICK_HZ` 64 for the
fixed integer step. State sends at 10 Hz. Voice sends at 50 Hz, from
the 20 ms Opus packets already in `modules/speech`. `rfd/0096` through
`rfd/0099` assumed one rate and produced 10.2 Mbit per second, which is
40 times the cap.

**An entity is a bone.** VRM 1.0 gives 55 humanoid bones plus 1 root,
so 56 per avatar, and only the root and hips translate. So `rfd/0002`'s
200 entities is 3.6 avatars, not 200 objects.

## Consequences

Interest management is required. Eight avatars fits. Forty does not.

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
- `rfd/0101`, for the measured zstd delta rate
