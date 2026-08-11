---
title: "RFD 0111: Convert the deployment words to the hexagon vocabulary"
rfd: "0111"
state: published
scope: architecture vocabulary across all repositories
---

## Problem

This stack names one component twice. RFD 0028 names its structure. A second
set of words names its deployment: plane, edge plane, and domain. A reader
must hold both sets and map between them. The second set has no RFD.
`lib/weft.ex` defines it, and more than ten READMEs copy the definition. The
two sets also give one word two meanings, for domain, for edge, and for port.
ASD-STE100 permits one meaning for one word.

## Decision

Retire plane, edge plane, and domain. The Netflix formulation supplies the
replacement for each one.

| retired    | replacement     | the meaning that carries over               |
| ---------- | --------------- | ------------------------------------------- |
| plane      | interactor      | a process that holds entities and actions   |
| edge plane | transport layer | the input that triggers an interactor       |
| domain     | service         | the set that shares a ring, and a machine   |
| store plane | data source    | the implementation behind a repository      |

The rules do not change with the words. An interactor opens no listening
socket. A transport layer holds no authority, runs no simulation, and keeps
no durable state. A service is the set of interactors that share a ring,
because a ring is shared memory and forces co-location.

"Control plane" and "data plane" stay. They come from networking, they name
a class of traffic, and neither names a process.

## References

- Netflix, "Ready for changes with Hexagonal Architecture":
  <https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749>
- Cockburn, the origin of the pattern:
  <https://alistair.cockburn.us/hexagonal-architecture>
- RFD 0028, amended by this RFD. `lib/weft.ex`, the `Weft` moduledoc.
- The term table, the collisions, and the rename list: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
