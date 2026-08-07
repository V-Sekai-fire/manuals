---
title: "RFD 0100: Tick rate is not send rate, and an entity is a bone"
rfd: "0100"
state: discussion
scope: zone-server-h2o, zone-guest-godot
---

## Problem

`rfd/0099` calculated 10.2 Mbit per second per client and called it
unshippable. That number is correct arithmetic on two wrong
assumptions.

The first assumption is that the send rate equals the tick rate.
`rfd/0096` through `rfd/0099` all divide by 15625 us, which is
`ZONE_TICK_HZ` at 64. Every one of them then assumed the server sends at
that rate too.

The second assumption is that an entity is a whole object. It is not.
An entity is a bone, or a part of a bone.

This RFD corrects both, adds the voice budget that no earlier RFD
counted, and states the resulting per-client target.

## Decision 1: three rates, not one

Simulation rate and send rate are separate numbers. Conflating them
produced the 10.2 Mbit per second figure.

There are in fact three rates, and each has a different reason:

| Rate       | Value       | Set by                                     |
| ---------- | ----------- | ------------------------------------------ |
| Simulation | 64 Hz       | `ZONE_TICK_HZ`, for the fixed integer step |
| State send | 10 to 20 Hz | this RFD, matching VRChat's IK range       |
| Voice send | 50 Hz       | 20 ms Opus packets in `modules/speech`     |

Voice already runs at 50 Hz in shipped code, which is faster than the
state send rate and slower than the simulation. That alone disproves
the idea that one rate governs everything.

VRChat is the closest comparable product, and it does not send at the
simulation rate. Its IK update rate is approximately 6 to 20 Hz, and
float parameters sync at approximately 10 Hz.

`ZONE_TICK_HZ` stays at 64, because the integer physics in
`zf_zonetick.h` wants a fixed step. The send rate becomes its own
constant, and it is 10 to 20 Hz.

The client covers the gap by interpolating, which is standard practice
and is what `rfd/0099`'s client-side prediction already implies.

## Decision 2: an entity is a bone, so the packet is mostly waste

`xr_grid_entity_packet_t` carries `pos_um_x/y/z` as three int64 values,
which is 24 bytes, and `rot_x/y/z` as swing-twist, which is 6 bytes.

VRM 1.0 defines 55 humanoid bones, of which 15 are required and 40 are
optional. An avatar also carries 1 root node for its world transform.
So the entity count per avatar is 56.

Two of those 56 use translation. The root places the avatar in the
world. The hips carry humanoid translation relative to that root. VRM
states that every remaining humanoid bone uses rotation.

So for 54 of 56 entities, the 24 bytes of position are unused. The real
payload for those is the 6-byte swing-twist rotation.

Per avatar:

    1 root     24 B position + 6 B rotation  =  30 B
    1 hips     24 B position + 6 B rotation  =  30 B
    54 others  6 B rotation each             = 324 B
    total                                    = 384 B

A 100-byte packet for each of 56 entities would cost 5600 bytes per
avatar. The rotation-only form costs 384 bytes, which is 14.6 times
smaller.

`rfd/0002`'s 200 entities per zone is therefore about 3.6 avatars, not
200 objects. That reframes every capacity claim in the earlier RFDs.

## Decision 3: bone level of detail is the form interest management takes

`rfd/0099` made interest management a requirement. This RFD says what
it does in a social VR context.

Distance does not only remove avatars. It removes BONES. A distant
avatar does not need 40 optional bones, because nobody can see a finger
at 20 metres.

Three tiers:

| Tier    | Entities sent               | Bytes | Rate  |
| ------- | --------------------------- | ----- | ----- |
| Near    | root plus 55 humanoid bones | 384 B | 20 Hz |
| Far     | root plus 15 required bones | 144 B | 5 Hz  |
| Distant | root only                   | 30 B  | 5 Hz  |

The 15-required and 55-total split is not invented here. It is VRM
1.0's own division, so a far-tier avatar remains a valid humanoid.

## Decision 4: voice is a first-class budget line, and it is mixed server-side

No earlier RFD counted voice. In social VR it is a large share of the
traffic, and leaving it out made every budget optimistic.

The codec choice is already made and already implemented.
`fabric-godot-core`'s `modules/speech` on branch `feat/module-speech`
uses Opus with these settings, from `speech_processor.h`:

| Setting                                  | Value                    |
| ---------------------------------------- | ------------------------ |
| `SPEECH_SETTING_CHANNEL_COUNT`           | 1, mono                  |
| `SPEECH_SETTING_SAMPLE_RATE`             | 48000                    |
| `SPEECH_SETTING_MILLISECONDS_PER_PACKET` | 20                       |
| `SPEECH_SETTING_BUFFER_FRAME_COUNT`      | 960                      |
| `SPEECH_SETTING_APPLICATION`             | `OPUS_APPLICATION_AUDIO` |

Two of those deserve review, and this RFD raises them rather than
changing them.

The module sets no bitrate. It never calls `OPUS_SET_BITRATE`, so Opus
selects its own default from the sample rate and channel count. For
48 kHz mono that lands near 64 kbps, which matches Discord's default.
The budget below uses 64 kbps for that reason, and an explicit constant
would be better than a library default.

The module also selects `OPUS_APPLICATION_AUDIO` rather than
`OPUS_APPLICATION_VOIP`. VOIP mode is the speech-tuned one. AUDIO mode
targets general content and generally needs more bitrate for equal
speech quality. Voice chat is the use case here, so this looks like the
wrong constant.

Industry rates for comparison:

| Use                        | Rate          |
| -------------------------- | ------------- |
| Clear speech               | 16 to 24 kbps |
| Most VoIP and conferencing | 24 to 64 kbps |
| Discord default            | 64 kbps       |
| Mumble maximum             | 128 kbps      |

Mix on the server, and send one stream. RP1's own demo used
server-mixed spatial audio.

The reason is arithmetic. Eight unmixed speakers at 24 kbps is 192 kbps
per listener, and it grows with the number of speakers. One mixed
stream at 64 kbps does not grow at all.

Server mixing costs CPU on a machine with one shared vCPU. Measure that
before committing to it, because `rfd/0096` measured the busy-poll
failure on exactly that machine shape.

`modules/speech` does not mix. It encodes, decodes, and buffers on the
client. Server-side mixing is unbuilt, and this RFD puts it on the
critical path.

## Decision 5: cost sets the cap, not client capacity

Every budget above asks what a client can receive. That is the wrong
question. The binding constraint is what the project can afford to
send.

Fly.io prices outbound transfer per GB:

| Region                               | Price per GB |
| ------------------------------------ | ------------ |
| North America and Europe             | 0.02 USD     |
| Asia Pacific, Oceania, South America | 0.04 USD     |
| Africa and India                     | 0.12 USD     |

A `shared-cpu-1x` machine with 256 MB costs 2.02 USD per month. Pay As
You Go has no free tier.

Take a 15 USD monthly budget. Two machines cost 4.04 USD, which leaves
10.96 USD for transfer. At 0.02 USD per GB that is 548 GB per month.

Now convert a per-client rate into client-hours:

| Per-client rate              | GB per client-hour | Client-hours for 548 GB | Concurrent, 24/7 |
| ---------------------------- | ------------------ | ----------------------- | ---------------- |
| 648.6 kbps, the budget above | 0.29187            | 1878                    | 2.6              |
| 320 kbps                     | 0.144              | 3806                    | 5.2              |
| 128 kbps                     | 0.0576             | 9514                    | 13.0             |
| 64 kbps                      | 0.0288             | 19028                   | 26.1             |
| 41.7 kbps                    | 0.01877            | 29200                   | 40.0             |

The budget in the previous section supports 2.6 concurrent users, run
continuously, for 15 USD per month. Comparing against VRChat's cap of
80 or Fortnite's 100 was therefore meaningless. Cost stops this design
roughly 30 times sooner than any of those product limits.

Reverse the calculation to get the requirement. Forty concurrent users
running continuously need 41.7 kbps per client. That is 15.5 times less
than 648.6 kbps.

Region multiplies the problem. Asia Pacific doubles the price, and
Africa and India multiply it by six. A client in India costs six times
a client in Europe for identical traffic.

### What 128 kbps actually buys

Take 128 kbps as a target, which gives 13 concurrent users
continuously, or approximately 475 users at 20 hours each per month.

Voice is the largest single line. At Opus 64 kbps it takes half the
budget. At 24 kbps, which the sources call clear for speech, it takes
19 percent.

With voice at 24 kbps, 104 kbps remains, which is 13000 bytes per
second. At a 10 Hz state send that is 1300 bytes per update:

    3 near   x 384 B = 1152 B
    1 far    x 144 B =  144 B
    total            = 1296 B

So 128 kbps buys about four visible avatars at 10 Hz, not forty.

That is the real design pressure. It points at three levers. Reduce the
voice bitrate. Reduce the state send rate. Compress the per-bone
rotation below 6 bytes.

### Consequence for decision 4

`OPUS_APPLICATION_AUDIO` with no explicit bitrate is now a cost
decision, not only a quality decision. The library default near 64 kbps
consumes half of a 128 kbps budget.

Set the bitrate explicitly, and evaluate `OPUS_APPLICATION_VOIP`
against it, because VOIP mode reaches speech quality at a lower rate.

## The corrected budget

Using 40 avatars, the tiers above, and server-mixed voice:

     8 near    x 384 B x 20 Hz = 61440 B/s = 491.5 kbps
    12 far     x 144 B x  5 Hz =  8640 B/s =  69.1 kbps
    20 distant x  30 B x  5 Hz =  3000 B/s =  24.0 kbps
    voice, server-mixed                    =  64.0 kbps
    total                                  = 648.6 kbps

Against the sources:

| Reference             | Rate                 |
| --------------------- | -------------------- |
| This design           | 648.6 kbps           |
| Fortnite              | 110 to 330 kbps      |
| Roblox                | 220 kbps to 1.3 Mbps |
| `rfd/0099` as written | 10.2 Mbit per second |

648.6 kbps sits inside Roblox's range and near twice Fortnite's upper
bound. It is defensible on client capacity, and decision 5 shows it
fails on cost.

Client capacity supports it. The Sony Bandwidth Probe found 95.5
percent of USA samples at or above 512 kbps download. It found 97.6
percent in Europe at or above 512 kbps. Those samples are from 2010, so
they are a conservative floor rather than a current estimate.

Upload is the tighter side, and it is tight. 97.3 percent of Americas
samples are at or above 128 kbps. A client sends only its own avatar,
which is 384 bytes at 20 Hz, or 61.4 kbps. Voice adds 24 to 64 kbps.

So a client uploads 85.4 to 125.4 kbps. That fits under 128 kbps, and
it fits with very little margin. An increase in send rate or bone count
removes clients from the design. It starts with the 2.7 percent below
128 kbps, and it takes more as the number grows.

## Consequences

`rfd/0099`'s 10.2 Mbit per second figure is superseded. The reasoning
was right and both inputs were wrong.

The send rate needs its own constant, separate from `ZONE_TICK_HZ`.
Name it explicitly so the two never merge again.

The wire form for a rotation-only bone should not carry 24 bytes of
unused position. Whether that is a second packet type or a flag on the
existing one is an implementation question, and this RFD does not
decide it.

Capacity claims stated in entities must say whether they mean bones or
avatars. At 56 entities per humanoid the two differ by a factor of 56.

Server-side voice mixing is now on the critical path, and its CPU cost
on `shared-cpu-1x` is unmeasured.

## Sources

- [Networking for Physics Programmers, GDC 2010](https://www.gamedevs.org/uploads/networking-for-physics-programmers.pdf), for the Sony Bandwidth Probe
- [VRM 1.0 humanoid specification](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/humanoid.md), for 55 bones, 15 required, hips-only translation
- [Opus, Hydrogenaudio Knowledgebase](https://wiki.hydrogenaudio.org/index.php?title=Opus)
- [Blueprint for the Open Metaverse](https://cdn.rp1.com/whitepaper.pdf), for server-mixed spatial audio
- `src/gen/xr_grid_entity_packet.h`, for the packet layout
