# RFD 0001: Zonefabric roadmap: PERT order, current status, and fps/eBPF/sandbox notes

**State:** discussion

## Summary

This RFD sequences the remaining `zone-server-h2o` zonefabric work by the
PERT critical path `decisions/20260806-pert-critical-path-zonefabric.md`
already established. It records a done, compiled-but-not-wired, or
not-started status for each ported RFD task, so a future contributor reads
one table instead of re-deriving it. It records a settled reference note
as context, not an open question: how this architecture compares to
Glenn Fiedler's `mas-bandwidth/fps` article-series code. It also records
two encoding decisions for CastSpell's sandbox boundary, the same
bitpacked struct format `RFD 0010` already chose for runtime data, and
CBOR-LD for package manifests, and a licensing
preference, Apache-licensed eBPF tooling, for later, currently-deferred
work.

## Background

`decisions/20260806-zone-server-h2o-replaces-godot-fabriczone.md` recorded
the decision to build `zone-server-h2o` and ported the zonefabric RFDs from
`weftspun/h2o-bench-tpcc`. That decision left two things unstated.

First, which of the now-ported RFD tasks the repo already finished today,
versus only scaffolded or unit-tested in isolation. Second, how this
architecture's scaling reasoning compares against `mas-bandwidth/fps`, the
companion code for a public article series on scaling a first-person
shooter's server architecture, so future capacity planning starts from a
reference point instead of a blank page.

## Motivation

Recording the status table and the reference notes here avoids three
failure modes. A future session re-derives the PERT order from
`decisions/20260806-pert-critical-path-zonefabric.md` from scratch, instead
of reading a checkable status table. A reader mistakes the `fps` kernel-bypass
comparison for a missing requirement, instead of a deliberately deferred
optimization. A future eBPF or effect-scripting task starts a new design
from zero, instead of reusing tooling the project already built and
accepted.

## Proposal

Adopt the existing PERT critical path — task A, task B, task C, task F,
task I, task M — as the build order for the remaining zonefabric work.
Record the current status of every task in the table below.

| Task | What it is                                | Status                                                  |
| ---- | ----------------------------------------- | ------------------------------------------------------- |
| A    | Binary value encoding                     | Done                                                    |
| B    | FDB keyspace and async callbacks          | Done                                                    |
| C    | Actor-lite worker pool                    | Done                                                    |
| F    | ZoneTick                                  | Done                                                    |
| D    | Slotmap entity storage                    | Not started                                             |
| G    | Zone-state blob persistence               | Not started                                             |
| H    | GhostRelevance (AOI query)                | Not started                                             |
| I    | CastSpell (effect and fanout)             | Not started                                             |
| J    | EntityMigration                           | Not started                                             |
| K    | ZoneSplit                                 | Not started                                             |
| L    | Macaroon plus XDP security                | Not started                                             |
| M    | Feature ablation                          | Not started                                             |
| N, O | Benchmark harness and scaling measurement | Not started                                             |
| —    | ReBAC (`src/gen/rebac.c`)                 | Compiled, unit-tested, not called from the request path |
| —    | Avatar IK (`src/gen/sinew_align.c`)       | Compiled, unit-tested, not called from the tick loop    |
| —    | Physics (`src/physics/mj_physics.c`)      | Compiled, unit-tested, not called from the tick loop    |

`src/zf_kv.c` covers only the `zf/zone/` and `zf/entity/` keys today. The
`zf/zone_state/`, `zf/effect/`, and `zf/fanout/` keys `RFD 0002
(zonefabric-scaling)` also describes remain unimplemented. TLS in `main.c`
still passes `NULL` for both the certificate and the key, so the server
accepts no client authentication yet.

`docs/0001-defer-nogod-gossip-authority.md`, in `zone-server-h2o` itself,
still describes the zone ID as a hardcoded value. Commit `a36bc8a` already
made the zone ID a required command-line flag, and nobody updated that doc
to match.

### fps comparison, as settled context

`weftspun/h2o-bench-tpcc`'s `rfd/0002-zonefabric-scaling.md` already
compares this design's shape against `mas-bandwidth/fps`. Four gaps stand
against it: no delta compression, no client prediction or rollback, no
real-time multicast or snapshot delivery path, and no kernel-bypass packet
ingest layer.

The kernel-bypass gap does not mean this design lacks UDP.
`decisions/20260501-webtransport-over-quic-for-game-traffic.md` already
puts WebTransport, and therefore QUIC and UDP, under all client-server game
traffic. The gap names only the absence of an ingest-layer optimization
that intercepts packets ahead of the normal kernel socket path, the way
`mas-bandwidth/fps` does with its own kernel tooling. The project already
filed that optimization as a future item, not a blocker for the current
milestone.

Every comparison in this RFD, and any future one, states the concept
`mas-bandwidth/fps` shows in this project's own words. A phrase like "a hub
server plus per-zone instances" is an example, and so is "a shallow
cross-server state cache." No comparison copies `mas-bandwidth/fps`'s code,
comments, file layout, or prose, since that project sits outside this
org and the project treats it as reference material only, the same way it
would treat any other unaffiliated open-source project it studies for
scaling ideas.

## Recommendation and next steps

List these follow-ups in PERT order.

1. Wire the three orphaned modules into the real request path. This work
   costs little and unblocks no other task, but it removes the ambiguity
   around otherwise-unused code. Call `rebac_check` from `wt_session` or
   from a real handler under `src/handlers/`. Drive `mj_physics_step` from
   `zf_zonetick.c` for entities that carry physics. Call `sinew_align` from
   an IK pipeline the tick loop calls.
2. Land task D, slotmap entity storage. The PERT slack analysis marks this
   task as near-critical, so build it early.
3. Land task G, the zone-state blob (a batched slotmap plus zstd
   persistence design), and task H, GhostRelevance, an AOI query. Neither
   exists in `zf_kv.c` today.
4. Land task I, CastSpell. This is the single riskiest task on the
   critical path: it carries the highest variance and three upstream
   dependencies. Stub the fanout radius scan first, per the PERT
   risk-mitigation note, and optimize it once the rest of the loop works.

   Reuse the project's existing sandboxed-execution work for CastSpell's
   effect step, rather than build a new execution engine.
   `decisions/20260611-generated-behavior-sandboxed-riscv.md` already runs
   generated enemy and ability behavior as sandboxed RISC-V programs
   through `feat/sandbox`, so a misbehaving program degrades one entity
   rather than the whole instance. `fabric-godot-core`'s `modules/sandbox`
   already embeds `libriscv` for this in the Godot client and editor
   tooling.

   Embed the same `libriscv` sandbox directly in `zone-server-h2o`, and let
   designers author CastSpell effects in GDScript, compiled to a RISC-V ELF
   binary through `godot-sandbox-gdscript-compiler`. This reuses tooling
   the project already built and its contributors already like, rather
   than inventing a bespoke effect-scripting system for task I.

   Generalize this pattern beyond CastSpell: any non-core code the server
   runs, generated behavior, CastSpell effects, and future mod or
   third-party content alike, loads as a sandboxed `libriscv` ELF binary,
   never as code the host process links or interprets directly. Package
   each ELF with a manifest that declares what the package needs before
   the host loads it: which helper functions and host capabilities it
   calls, its entry points, and a version. `zone-server-h2o` treats the
   manifest, not the ELF alone, as the unit the host validates and grants
   capabilities to.

   The sandbox FFI boundary between the host and each loaded package
   reuses the same manually written, bitpacked struct format
   `zf_zonetick.c` already stores entities in, rather than add a third
   binary format such as FlatBuffers or protobuf alongside it. The
   project keeps exactly two encodings, not four: this bitpacked struct
   format for every nasty-layer surface (the zone tick and the CastSpell
   FFI alike), and CBOR-LD, below, for every cheap-layer surface.

   A host binary and a sandboxed package binary still come from separate
   builds, often from separate sources (a designer's GDScript compile, a
   future third-party mod), so a reader compiled against an older struct
   layout still needs a way to detect a newer, incompatible writer.
   Solve that with an explicit ABI version field inside the manifest
   (below), not with a self-describing runtime format. The host reads
   that field, and refuses to load a package whose declared ABI version
   does not match the struct layout the host itself was built against.
   `RFD 0010` already accepted the matching tradeoff for the zone tick,
   manual struct versioning instead of a self-describing format; this
   extends the same discipline to the CastSpell FFI, rather than
   introduce a second binary format and a `flatc` build dependency to
   solve the same problem a different way.

   The manifest itself, separately from the bitpacked-struct runtime
   data it describes, is a good fit for CBOR-LD, decoding to plain
   JSON-LD, itself plain JSON. Two properties argue for that choice over
   a bespoke manifest format. First, `zone-server-h2o` and its neighboring
   repos already use MCP tooling (`vsekai-godot-mcp`), and MCP's own wire
   format is JSON-RPC, so a manifest that decodes straight to JSON needs
   no translation layer to list, validate, or inspect through an MCP
   tool. Second, a manifest's capability declarations name concepts a
   package needs from the host, and JSON-LD's context mechanism gives
   those concept names a shared, linkable vocabulary across packages and
   across repos, the same property CBOR-LD's designers built it for in
   verifiable-credential use cases. This is a narrower, metadata-only use
   of CBOR-LD; it does not touch the entity or effect data itself, which
   stays bitpacked-struct-encoded for the reasons above.

   Record one determinism note on CBOR-LD, since a manifest is a natural
   candidate for content-addressed or write-once storage, and the base
   CBOR-LD 1.0 specification itself does not define canonical or
   deterministic encoding. It reuses JSON-LD's own processing determinism
   for term mapping, not RFC 8949's byte-level deterministic CBOR rules
   (shortest-form integers, no indefinite lengths, lexicographically
   sorted map keys). If a manifest ever needs a stable hash, for a
   content-addressed package store or an append-only audit trail, encode
   it under RFC 8949 section 4.2's deterministic CBOR rules on top of
   CBOR-LD's compression, the same layering `w3c.github.io/vc-barcodes`
   already ships: a fixed, non-negotiated term registry, plus an explicit
   hash computed over a defined set of fields, rather than CBOR-LD's base
   spec alone. This note matters once a manifest needs permanent storage;
   it does not block landing task I without one.

   Record one implementation constraint alongside the encoding choice:
   `zone-server-h2o` builds under Fil-C, a memory-safe C toolchain, not
   Rust or C++, and the mainstream CBOR-LD ecosystem runs on JavaScript,
   Java, and Rust. No mainstream, production-grade C library implements
   the full W3C CBOR-LD compression algorithm today.

   Reject a hand-maintained, fixed term-to-integer table as a substitute
   for real CBOR-LD, even though it would run in pure C with no
   dependency added. A fixed table encodes plain CBOR with a private
   dictionary, not CBOR-LD: it drops JSON-LD's actual context processing,
   the property this RFD picked CBOR-LD for in the first place, shared,
   linkable vocabulary any conformant JSON-LD tool can decode, not only
   this project's own tooling. `w3c.github.io/vc-barcodes` still uses a
   real, registered CBOR-LD term mapping, not an ad hoc one invented
   outside the spec, so a private table here would not match that
   precedent either.

   Split the manifest pipeline across two roles instead, so a real
   JSON-LD processor never has to run inside `zone-server-h2o`'s own
   pure-C runtime process. At package-build time, alongside
   `godot-sandbox-gdscript-compiler`'s own compile step, a separate
   authoring tool assembles `jsonld-cpp` (a C++14, spec-compliant W3C
   JSON-LD 1.1 processor) with `zcbor` or `QCBOR`, writing the W3C
   CBOR-LD compression algorithm's term-mapping step by hand on top of
   `jsonld-cpp`'s real context processing, and produces a genuinely
   spec-compliant CBOR-LD manifest as build output. This tool runs
   offline, outside the deployed server, so its C++ dependency never
   touches `zone-server-h2o`'s own build or runtime.

   At load time, inside `zone-server-h2o` itself, the host only decodes
   already-produced CBOR-LD bytes; it never re-runs JSON-LD context
   resolution. Decoding plain CBOR back out needs no JSON-LD processor at
   all, so the pure-C runtime constraint holds here: use `QCBOR` (or
   `zcbor`'s generated decoder) inside the host process, in pure C under
   Fil-C, to read the manifest's fields once a package build already
   produced them.

   This keeps the manifest genuinely CBOR-LD, keeps the C++ dependency
   confined to an offline authoring tool this project's deployed binaries
   never link, and keeps the deployed runtime pure C throughout.

   Also rejected: `gitlab.com/coswot/cborld-c`, the one existing pure C,
   batteries-included implementation of the full CBOR-LD compression
   algorithm, from the CoSWoT research group, and the one path that would
   have kept even the offline authoring tool free of a C++ dependency.
   It ships under the CeCILL v1.1 license, a strong-copyleft license,
   which conflicts with this project's preference for permissive
   licensing elsewhere (see the `iovisor/ubpf` note above). It also reads
   as a research and embedded prototype rather than a vetted production
   dependency. Revisit it only if `jsonld-cpp` plus `zcbor`/`QCBOR` turns
   out not to fit the offline authoring tool well in practice.

   Name the design principle behind the bitpacked-struct-versus-CBOR-LD
   split, rather than leave it implicit: the "Cheap or Nasty" pattern
   from the ZeroMQ guide (`zguide.zeromq.org`, chapter 7). That pattern
   splits any protocol into a cheap layer, self-describing, synchronous,
   low-volume, and tolerant of frequent change, and a nasty layer,
   hand-optimized binary, asynchronous, high-volume, and resistant to
   change. The guide warns against compromising between the two inside
   one format, since the tradeoffs each layer needs run in opposite
   directions.

   This project already applies that split once, at the transport level:
   `decisions/20260612-fabric-channels-as-reliability-classes.md` gives
   `CH_MIGRATION` reliable-ordered delivery for control and state, and
   `CH_INTEREST` unreliable delivery for transforms, so control traffic
   and high-volume data traffic never share one reliability model. The
   manifest-versus-runtime-data split above extends the same principle
   one layer down, to the encoding itself: CBOR-LD serves the cheap
   layer, low-volume manifests an MCP tool might inspect, and the
   bitpacked struct serves the nasty layer, the zone tick and the
   CastSpell FFI data a host and a sandboxed package exchange many times
   a second. Protobuf and FlatBuffers both sit outside this project's two
   chosen formats: protobuf's build-time compiler step duplicates what
   CBOR-LD already gives the cheap layer, and FlatBuffers' schema
   evolution duplicates what the manifest's ABI version field already
   gives the nasty layer, so neither earns a third format's added build
   dependency.

5. Type the CastSpell sandbox boundary, and extend `RFD 0010
(binary-value-encoding)`, with a primitive-versus-reference split. Reuse
   the value-type vocabulary the `gltf_interactivity` specification, vendored
   under `taskweft/thirdparty/gltf_interactivity/`, already defines, rather
   than invent a new one.

   That specification splits every value into two kinds. Primitive types
   carry a value directly: `bool`, `float`, `float2`, `float3`, `float4`,
   `float2x2`, `float3x3`, `float4x4`, and a 32-bit signed `int`. The `ref`
   type carries an opaque reference instead, with a null reference as its
   default value.

   Map `ref` onto the slotmap's generational entity handles from `RFD 0017
(slotmap-entity-storage)`, and map the primitive types onto plain
   numeric fields such as position, velocity, and health. Represent this
   split inside the bitpacked struct layout item 4 introduces: a
   primitive field holds its value inline, and a `ref` field holds a
   slotmap handle, at a fixed offset the manifest's ABI version field
   pins down. This split gives the sandbox FFI boundary, and any future
   CastSpell parameter encoding, a clean value-versus-handle distinction
   the project already uses elsewhere, instead of a new one built from
   scratch.

6. Defer these tasks, per the PERT slack analysis: task E, zstd (11.1 days
   of slack), task L, Macaroon plus XDP (7.5 days of slack, and this task
   can run in parallel with other work), task J, EntityMigration (stub this
   as "stay in the birth zone" at first), and task K, ZoneSplit.

   Record one licensing note here, for task L and for the kernel-bypass
   ingest layer named above. Both stay deferred, not blocking. Linux's
   native `libbpf`/`libxdp` stack sits close to the GPL-licensed kernel
   tree, since several kernel eBPF helpers need a GPL-compatible program
   license before the kernel loads them.

   `iovisor/ubpf` gives an Apache-2.0 alternative: a userspace eBPF virtual
   machine with an interpreter and a JIT compiler for x86-64 and ARM64.
   `ubpf` carries no built-in verifier of its own, so a future adopter
   pairs it with an external verifier such as PREVAIL. `ubpf` carries no
   dependency on the Linux kernel GPL boundary, since it runs entirely in
   userspace. Prefer embedding `ubpf` directly over routing through
   `microsoft/ebpf-for-windows`, since that project only wraps `ubpf` for
   Windows hosts, and this project targets Linux and `libh2o`. Treat this
   as a licensing note to carry forward, not a task to start now.

7. Fix the stale claim in `docs/0001-defer-nogod-gossip-authority.md`, in
   `zone-server-h2o`. That doc still describes the zone ID as hardcoded.
   Commit `a36bc8a` and the current `main.c` already contradict that claim.
8. Replace the stale, TPC-C-flavored `test/verification/README.md` with
   zonefabric-specific invariants: entity migration, ghost consistency, and
   journal replay. Add these as those features land, per task M.
9. Wire real TLS certificate and key material before any real
   client-handshake test runs. `main.c` still passes `NULL` for both today.

## Open questions and verification

A future session checks this RFD's claims still hold this way. Re-run the
local equivalent of `zone-server-h2o`'s `real-build.yml`. Grep `src/` for
calls to `rebac_check`, `mj_physics_step`, and `sinew_align`; zero calls
exist outside the unit tests today, so this check reveals whether the
wiring work in item 1 above happened. Check `zf_kv.h`'s own scoping
comment, and confirm whether the `zf/zone_state/`, `zf/effect/`, and
`zf/fanout/` keys exist yet.

Open question: does the sandboxed-CastSpell approach in item 4 above need
its own follow-up RFD once `libriscv` integration work starts in
`zone-server-h2o`, given the scope difference between a client-side sandbox
and a server-side one running under load. This RFD does not resolve that
question, and records it here for whoever picks up task I.

Open question: item 4's manifest format needs an actual schema, a
concrete list of declarable capabilities and host helper functions, an ABI
version field, and a validation step the host runs before granting those
capabilities to a loaded package. This RFD decides the manifest's
encoding, CBOR-LD, and reuses `RFD 0010`'s bitpacked struct format for the
FFI data, but does not design the schema itself. Confirm, before task I
lands, whether `godot-sandbox-gdscript-compiler`'s own ELF output already
carries any manifest-like metadata this project can reuse, rather than
build a second one alongside it.

Open question: if a manifest ever needs write-once or content-addressed
storage, confirm whether RFC 8949 section 4.2's deterministic CBOR rules,
layered on top of CBOR-LD, give a sufficient canonical form, or whether
the project needs `w3c.github.io/vc-barcodes`'s fuller pattern instead, a
fixed term registry plus an explicit hash over a defined field set.

Open question: confirm, before task I lands, that `jsonld-cpp` still
builds and maintains cleanly as an offline authoring-tool dependency, and
design the offline tool's own build so it never becomes part of
`zone-server-h2o`'s own CMake target, per `RFD 0010`'s and item 4's other
tradeoffs above.

Open question: confirm whether QCBOR's development branch has landed full
RFC 8949 section 4.2 map-key-sorting support by the time this project
needs a hashable manifest encoding, since QCBOR's current stable 1.x
release does not sort map keys yet; `zcbor`'s generated decoder gives
deterministic key order regardless, from the schema, and stays the
preferred choice for the in-host decode step if that QCBOR work has not
landed.
