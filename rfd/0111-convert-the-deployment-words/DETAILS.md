## Context and problem statement

RFD 0028 made every component a hexagon with a `core/` + `ports/` +
`adapters/` layout. It took the pattern from Cockburn and added four words
that Cockburn does not use: core, domain logic, edges, and the `*_source` /
`*_sink` pair.

A second vocabulary grew later, in code rather than in an RFD. The `Weft`
moduledoc in `fabric-weft-plane` defines plane, edge plane, and domain. Ten
or more READMEs repeat those definitions. `fabric-zone-domain` and
`fabric-behaviour-domain` carry the same sentence word for word.

`fabric-harness` states the risk in its own README: a decision written twice
drifts, and the stale copy still reads as authoritative. `Weft.VocabularyTest`
exists to catch that. It reads the files of one git repository only, and it
finds only retired words, so a live word with two meanings is invisible to it.

## Decision drivers

- ASD-STE100 permits one meaning for one word. RFD 0000 applies STE to all
  prose here.
- `Weft` states the same rule, and applied it once already. Khronos CATSG
  says "entity" for the controlling human or AI. weft says "controller",
  because entity already names the simulated unit.
- Cockburn writes about the inside of one component. He gives no word for a
  process or a machine. Netflix writes about the same inside, in the
  microservice framing, and gives nouns this stack can use.
- Two names for one component cost more than the deployment words earn. A
  reader of `fabric-authority-plane` has to learn that a plane is a process,
  that the process holds a tick, and that the tick is what RFD 0028 calls
  the inside. One name removes two of those steps.

## The Netflix terms

The article defines five terms. Each quotation below is from it.

| term            | definition                                                                                               |
| --------------- | -------------------------------------------------------------------------------------------------------- |
| Entity          | "domain objects (e.g., a Movie or a Shooting Location) — they have no knowledge of where they're stored" |
| Repository      | "interfaces to getting entities as well as creating and changing them"                                   |
| Interactor      | "classes that orchestrate and perform domain actions"                                                    |
| Data source     | "adapters to different storage implementations"                                                          |
| Transport layer | "can trigger an interactor to perform business logic. We treat it as an input for our system"            |

The rule that holds them together is that all dependencies point inward.

## The conversion

| retired word | replacement     | why the replacement fits                                                    |
| ------------ | --------------- | --------------------------------------------------------------------------- |
| plane        | interactor      | a plane holds entities and the actions on them, and it holds no transport   |
| edge plane   | transport layer | an edge plane terminates a transport and triggers an interactor             |
| domain       | service         | the microservice is the unit that deploys, and the ring decides its members |
| store plane  | data source     | it implements repositories over FoundationDB and SQLite                     |

"Service" is the weakest of the four, because the Netflix article names
microservices without defining one. It is the only deployment word the
formulation has, and the ecosystem uses it the same way. This RFD takes it
and states the local meaning: a service is the set of interactors that share
a ring.

## One name for one concept

| word            | the one meaning                                           | source   |
| --------------- | --------------------------------------------------------- | -------- |
| entity          | one simulated thing in a zone, with position and velocity | weft     |
| repository      | an interface that gets, creates, and changes entities     | Netflix  |
| interactor      | a process that performs actions on entities               | Netflix  |
| data source     | an implementation of a repository                         | Netflix  |
| transport layer | the input that triggers an interactor                     | Netflix  |
| service         | the set of interactors that share a ring                  | Netflix  |
| ring            | the iceoryx2 shared memory bus                            | weft     |
| port            | a TCP or UDP listening socket                             | ordinary |
| actor           | a runtime process with a single writer                    | weft     |
| controller      | the human or the AI that controls an avatar               | weft     |

weft and Netflix agree on "entity". Netflix says an entity does not know
where it is stored. weft says an entity is the unit the data plane moves.
Both keep the entity away from its storage, so one meaning covers both.

## Where the terms land in this stack

| the thing that exists today                        | the word for it |
| -------------------------------------------------- | --------------- |
| `XRGridEntityPacket` from `lean-entity-packet`     | entity          |
| `src/authority_tick.c` in `fabric-authority-plane` | interactor      |
| the reducer in `combat`, the roll in `loot`        | interactor      |
| `fabric-gateway-edge`, `fabric-ingest-edge`        | transport layer |
| `Weft.Actor.Store`, the store API                  | repository      |
| FoundationDB behind the SQLite VFS                 | data source     |
| `fanout_sink_t` in `fabric-fanout-edge`            | repository      |
| the WebTransport sink behind it                    | data source     |
| a recorded fixture under CI                        | data source     |
| the members of `fabric-zone-domain`                | one service     |

`fabric-fanout-edge` shows that the pattern is in the code already. Its
README says that a WebTransport sink can replace the default sink, and that
nothing above it changes. That is one repository with two data sources.

## The collisions this resolves

The word "domain" had three meanings: the deployment packing, the "domain
logic" of RFD 0028, and a field on the wire in RFD 0091. The first becomes
"service". The second becomes "entity" and "interactor". The third needs its
own decision, because a change on the wire is a protocol change.

The word "edge" had two meanings. RFD 0028 said "concrete I/O at the edges",
and an edge plane was a process. RFD 0028 now says "outside the interactor",
and the process is a transport layer. No meaning is left to collide.

The word "port" had two meanings. Netflix uses no word "port", so the
listening socket keeps it, and `fabric-zone-domain` needs no edit.

## The collision this creates

Netflix says "repository" for an interface to entities. This project says
"repository" for a git repository, in RFD 0000, RFD 0062, RFD 0063, and
RFD 0064. That is a new word with two meanings, and this RFD makes it.

The resolution is to write "git repository" in full every time, and to keep
"repository" alone for the interface. Keeping Cockburn's word "port" for the
interface would avoid this, and it would revive the collision with the
listening socket, which is in the code of every transport layer. A collision
in prose costs less than a collision in code.

## What "plane" keeps

"Control plane" and "data plane" stay whole. They come from networking, they
name a class of traffic, and neither one names a process. `Weft.DataPlane`
keeps its name. Bare "plane", as a noun for a process, is retired.

## The rename list

Fifteen git repositories carry a retired word in the name.

| now                       | after                         |
| ------------------------- | ----------------------------- |
| `fabric-authority-plane`  | `fabric-authority-interactor` |
| `fabric-crowd-plane`      | `fabric-crowd-interactor`     |
| `fabric-taskweft-plane`   | `fabric-taskweft-interactor`  |
| `fabric-motion-plane`     | `fabric-motion-interactor`    |
| `fabric-janet-plane`      | `fabric-janet-interactor`     |
| `fabric-tool-plane`       | `fabric-tool-interactor`      |
| `fabric-weft-plane`       | `fabric-weft-interactor`      |
| `fabric-store-plane`      | `fabric-store-datasource`     |
| `fabric-gateway-edge`     | `fabric-gateway-transport`    |
| `fabric-ingest-edge`      | `fabric-ingest-transport`     |
| `fabric-fanout-edge`      | `fabric-fanout-transport`     |
| `fabric-asset-edge`       | `fabric-asset-transport`      |
| `fabric-zone-domain`      | `fabric-zone-service`         |
| `fabric-behaviour-domain` | `fabric-behaviour-service`    |
| `fabric-store-domain`     | `fabric-store-service`        |

GitHub redirects a renamed git repository, so a `git subtree` remote and a
Lake `require ... from git` continue to resolve. Each pin gets updated in the
same pass.

Three git repositories hold the RFD 0028 triad on disk: `loot`, `combat`,
and `progression`. Each `core/` becomes `entities/`, each `ports/` becomes
`repositories/`, and each `adapters/` becomes `datasources/`.

Five git repositories carry "core" in the name: `lean-shared-core`,
`lean-rebac-core`, `lean-combat-core`, `lean-loot-core`, and
`lean-progression-core`. Each becomes `lean-*-entities`.

## A gap this pass found

The `lean-*-core` READMEs state a "Hexagon layout" of `core/`, `ports/`, and
`adapters/`. Those directories do not exist. Each of those git repositories
holds one Lean namespace directory, such as `Shared` or `Rebac`. The
documents describe a layout that no git repository has. The rename pass
corrects the READMEs to the directories that are there.

## Consequences

- One component has one name. A reader learns one vocabulary.
- Each word has one meaning, and STE holds across the git repositories.
- The definitions leave the READMEs and live here, so the copies stop
  drifting.
- `Weft.VocabularyTest` gains the retired words: plane, edge plane, domain,
  core, and domain logic. The test then holds this decision. The entries for
  "control plane" and "data plane" must not match, so the pattern needs a
  word boundary and a check for the preceding word.
- The rename touches fifteen git repository names, three directory triads,
  five more names, and every README that copies a definition. Every one is
  mechanical, and none changes a build.
- This RFD does not rename the `domain` field on the wire in RFD 0091. That
  is a protocol change and needs its own RFD.
