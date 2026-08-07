---
title: Godot client transport handshake against the authoritative server
date: 2026-05-06
status: accepted
decision-makers: K. S. Ernest (iFire) Lee
tier: baseline
---

> Moved to [rfd/0010](../rfd/0010-maglev-cycle-1-gateway-handshake/README.md).

# Godot client transport handshake against the authoritative server

## The Context

The clients in this stack are Godot engine processes built from the frozen Godot 4.7 "double" engine ([pin the engine](20260606-pin-engine-to-frozen-godot-4-7.md)). Godot's own networking — its multiplayer peer, thread model, and datagram path — carries every later networking behaviour, so a non-Godot ping (curl, Python, an Elixir harness) tests the wire but leaves the engine's own client path unproven. Engine-specific datagram and connection bugs surface only when a real Godot process drives the transport.

## The Problem Statement

Until a real Godot client opens a connection to the authoritative server and completes the round trip — connect, receive, exit cleanly — the client side of the networking stack is unvalidated. A failure first seen deep in a gameplay scene is far harder to isolate than the same failure seen in a bare handshake.

## Design

A minimal headless Godot client opens a transport connection to the authoritative server, waits for the server's first message, logs it, and exits cleanly. Running headless isolates client networking from display and input.

Transport is switchable in the client ([WebTransport over HTTP/3](20260606-webtransport-http3-transport.md), [fabric channels as reliability classes](20260612-fabric-channels-as-reliability-classes.md)): ENet for a stable local default, or WebTransport/QUIC under `TRANSPORT=wt`. The same handshake holds across both — the client calls `create_client(host, port)` for ENet or `create_client(host, port, "/wt")` for WebTransport and joins once the peer reports connected. The client reaches the authoritative server directly; no separate proxy tier sits in the path.

Pass criteria:

- The Godot client establishes the connection without TLS or handshake error.
- The client receives and logs the server's first message.
- The client exits cleanly: no orphaned process, no open port.

## The Downsides

A minimal Godot client is more work than a curl or harness ping, and the work cannot be skipped — a non-Godot client would not catch Godot-specific datagram handling before it reaches a gameplay scene.

## The Road Not Taken

- A bare non-Godot client (curl, Python, or Elixir harness): it tests the server in isolation and leaves the Godot client's transport path unverified until a gameplay scene exercises it, where a failure is much harder to isolate.
- A separate gateway proxy fronting the server on a privileged port: the as-built path connects the client straight to the authoritative server, so a proxy tier adds an unproven hop the slice does not need.

## Confirmation

The loop-slice client (`godot-loop-slice/client.gd`) completes this handshake against the authoritative server (`godot-loop-slice/server.gd`). The playable-loop smoke runs four real Godot clients through it end to end on ENet: each connects, joins, runs the loop, and exits cleanly. The run on 2026-06-29 passes — all four clients complete and exactly one loot grant lands. The WebTransport/QUIC path is selectable with `TRANSPORT=wt` over the same handshake.
