---
title: "RFD 0116: The client is native, from fabric-godot-core's gyre branch"
rfd: "0116"
state: published
scope: the Queen of the Gyre, and what a player runs to reach her
---

## Problem

RFD 0112 put the Queen's client in a browser. It chose Lexical for the slash command field,
because the field is the hard half: a parameter has to show as an inline block the caret
crosses in one key press, and an `<input>` holds plain text only. That reasoning was sound and
the field was built. RFD 0112 is abandoned anyway, because the field was the wrong thing to
optimise for.

A browser client is a second implementation of everything below the field. `client/src/cbor.js`
decodes what the ward publishes, in a language that shares nothing with the decoder the rest of
the fabric uses. It reaches the ward over a WebTransport stack that is not the one the ward
speaks, only compatible with it. It carries a toolchain — npm, esbuild, Playwright — that
nothing else in the domain needs. And it cannot enter XR, which is what the setting is for.

## Decision

The client is a Godot build from `fabric-godot-core`, branch `gyre`. `.meta` already pins that
branch, which is why the entry was the only one in the manifest that stated one.

The branch carries the parts already. `modules/http3` gives `WebTransportPeer` over a picoquic
backend, which is the stack `queen`'s `src/wt.c` terminates and the one `fabric-gateway-edge`
vendors — one QUIC implementation and one TLS library on both ends, rather than two that agree.
`modules/xr_grid` gives `XRGridEntityPacket`, the same 100-byte packet the ward writes and the
one `lean-entity-packet` specifies, so the client decodes with the fabric's decoder instead of a
second one. `modules/multiplayer_fabric` gives `FabricMultiplayerPeer`, the zone and the
snapshot. Nothing in this decision is new code in the engine; it is a decision about which
client is the client.

The slash command field is a `Control`, and RFD 0112's hard half stops being hard for the reason
it was hard: a caret in a `contenteditable` is a browser problem, and there is no browser.

The ward does not change. `queen serve` already speaks WebTransport, a datagram is already one
message, and the Queen already terminates QUIC in her own process. What changes is who connects.

## Consequences

RFD 0112 is abandoned. `fabric-store-domain/client` — Lexical, esbuild, the Playwright specs and
the JavaScript decoder — stops being the client. Removing it is its own change in its own
repository and is not assumed by this document.

The cost is a build. A browser client is served; a native client is compiled per platform from
an engine fork, which is slower to produce and heavier to distribute. That is accepted, because
the alternative was paying for a second decoder and a second transport forever to avoid paying
for a build once.

## References

- RFD 0112 chose the browser client and is abandoned. RFD 0085 holds the setting.
- RFD 0111 sets the words transport layer and service. RFD 0047 is why the Queen terminates
  QUIC herself rather than behind a bridge.
- `lean-entity-packet` specifies the 100-byte packet both ends now share.
- The module mapping, the transport path, and what happens to the web client: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
