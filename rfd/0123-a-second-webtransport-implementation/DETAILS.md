## What the second implementation found

Three disagreements, each measured on 2026-08-17, macOS arm64, against `pywebtransport` 0.20.1 and
`iceoryx2` 0.9.3 over a loopback session. None is fixed, and each is recorded in the `OPEN_GAPS.md`
of the repository that found it.

### A 64-entity slice does not fit in one datagram

`transport-fanout/src/fanout.h:39` caps a subscriber's slice and states the reason: "Cap one
subscriber's slice so a single write stays inside a datagram-sized batch. 64 entities \* 100 bytes
= 6400 bytes, comfortably inside one message."

A binary search over `send_datagram` on a live session puts the largest accepted datagram at
**1161 bytes**, which is **11** whole 100-byte records.

| payload    | records | result                             |
| ---------- | ------- | ---------------------------------- |
| 100 bytes  | 1       | delivered                          |
| 1161 bytes | 11      | delivered, and the largest that is |
| 1162 bytes | 11      | refused                            |
| 6400 bytes | 64      | refused                            |

6400 bytes is 5.5 times the measured limit. `datasource-queen/src/wt.c:32` sets `WT_MTU_MAX` to
1300, which is 13 records, so the C side's own configuration contradicts the C side's comment
before this implementation is considered. `transport-fanout` has never run and
`transport-ingest-c` has no `main`, so nothing had exercised the claim.

The limit is a negotiated QUIC value rather than a `pywebtransport` constant, so another path may
differ, and no measurement on another path exists. What stays open is whether
`MAX_SLICE_ENTITIES` is wrong, whether slices belong on streams, or whether `fanout_one`'s silent
truncation at 64 was always the real cap. `transport-ingest-python` splits a slice at 11 records so
that it runs, which is a decision the record does not yet justify.

### pywebtransport rejects EC server keys

`contract-wt/README.md` records the Godot demo server building "a fresh self-signed P-256
certificate on every run". `pywebtransport` refuses to open a listener with one, failing with
"failed to parse private key as RSA, ECDSA, or EdDSA". PKCS#8 keys from LibreSSL 3.3.6:

| key                   | result                                       |
| --------------------- | -------------------------------------------- |
| EC prime256v1 (P-256) | rejected                                     |
| EC secp384r1 (P-384)  | rejected                                     |
| RSA 2048              | accepted                                     |
| Ed25519               | untested; LibreSSL 3.3.6 cannot generate one |

Each end's key is its own, so this does not stop the two talking. It does stop the Python pair
serving a role the Godot side serves today, and which end is wrong is unresolved.

### A default iceoryx2 subscriber drops the oldest of three sends

`iceoryx2` defaults a subscriber's buffer to **2** samples with safe overflow on. Three records
published in a burst arrived as two, and the missing one was the oldest, before any reader was
slow. Both repositories now set the buffer explicitly and keep safe overflow, because RFD 0108
requires that a lagging reader never stall the writer.

The drop stays undetectable. `HeaderPublishSubscribe` carries a node id, a publisher id and an
element count, and no sequence number, so nothing distinguishes a dropped sample from one never
sent. RFD 0108 says a subscriber whose cursor falls out of the ring "receives a resync signal
rather than a gap"; no such signal exists, and defining one is a wire decision.

## The renames

Two repositories renamed, two created. GitHub redirects the old names.

| before              | after                      | path                         |
| ------------------- | -------------------------- | ---------------------------- |
| `transport-gateway` | `transport-gateway-c`      | `1-transport/gateway-c`      |
| `transport-ingest`  | `transport-ingest-c`       | `1-transport/ingest-c`       |
| —                   | `transport-gateway-python` | `1-transport/gateway-python` |
| —                   | `transport-ingest-python`  | `1-transport/ingest-python`  |

`check_path_recomposes` in `check_docs.py` requires the directory and its child to rebuild the
repository name, and all four do. The manifest count moves from 45 to 47.

Both C repositories carried a description using a word RFD 0111 retired — "hands the result to a
**plane** over iceoryx2" — because the READMEs were converted and the GitHub descriptions were
missed. Both now say interactor.

`check_docs.py`'s moved-repository check found eight stale references in six files across five
repositories, each fixed in its own pull request: `transport-fanout`, `transport-gateway-c`,
`transport-ingest-c`, `interactor-ward`, `entities-gyre` and `datasource-queen`.

## Why the language and not the library

RFD 0111 retires names that say how a thing was built, and `-c` and `-python` are exactly that. The
rule targets directories that collect whatever nobody classified: `service/`, `lean/`, `engine/`,
`vendor/`. Two repositories implementing one contract are a different case, because the build is
the only thing that separates them and the role word is already taken by both.

`transport-picoquic`, which RFD 0111 renamed from `fabric-edge`, is the precedent for naming a
transport repository after its stack, taken for the same reason: "Bare `transport` would read as a
name that went missing."

The language outlives the library. Swapping picoquic for another C QUIC stack, or `pywebtransport`
for aioquic, leaves both names true, where `-picoquic` and `-pywebtransport` would strand.

## What is built

Both repositories carry the conformance gate and the terminator, and neither carries a cross-test.

`conformance.py` decodes all 64 golden vectors, checks the fields the CSV names, and re-encodes to
compare byte for byte. `--self-test` corrupts one vector and the gate is wrong if that passes. CI
runs both, on every pull request and in the merge group.

`transport-ingest-python` was driven end to end on a live session: three records in one datagram
reached the ring byte-identical to the wire, and a 250-byte datagram was dropped whole rather than
trimmed to two records.

The live cross-test against the C pair is not written, and there is nothing yet to write it
against. `transport-gateway-c` and `transport-ingest-c` have no `main` and no `CMakeLists.txt`, and
both READMEs say "State: not started". `transport-ingest-c`'s copy of the transport code is a stale
fork of `transport-gateway-c`'s: it passes an `h3zero_callback_ctx_t` where `h3zero_callback` casts
to `picohttp_server_parameters_t`, and it lacks the `h3zero_declare_stream_prefix` call. That
divergence is the reason both Python repositories consume one emitted codec rather than two copies.
