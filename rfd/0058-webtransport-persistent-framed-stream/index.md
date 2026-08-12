---
title: "RFD 0058: WebTransport reliable delivery on one persistent framed stream per session"
rfd: "0058"
state: abandoned
scope: webtransportd WebTransport transport adapter
---

## Status

There is no framed stream. WebTransport carries message boundaries
already: a datagram is one message, and a stream's FIN is where its
message ends. So reliable traffic takes one bidirectional stream per
message and is read to `picohttp_callback_post_fin`, unreliable
traffic takes one datagram per message, and an unreliable stream that
needs sequencing carries the application's own counter in its own
payload. A length prefix in front of data that already knows where it
stops is redundant, and it hides the boundary the transport gives for
nothing.

The silent server this record was written to fix has a different
cause. `picowt_set_transport_parameters`, which runs per connection,
raises `initial_max_stream_id_bidir` and `initial_max_stream_id_unidir`
to `0x3F` along with the flow control limits.
`picowt_set_default_transport_parameters`, which runs once for the
`picoquic_quic_t`, raises neither — it sets only
`is_reset_stream_at_enabled` and `max_datagram_frame_size`. A server
configured through the second one gets no extra stream credit, so a
stream per message exhausts it, the exhausted credit blocks the
connect-accepted response on the control stream, and the fourth
session never finishes its handshake. That is the symptom this RFD
describes. The fix is the per-connection call, not a wire format.

This RFD stays as the record of the failure and of what was tried.
The scope line names `webtransportd`, which `rfd/0047` abandons.

## Problem

The picoquic WebTransport server goes silent once four or more
sessions connect. A fresh bidirectional stream per reliable message
uses up the connection's stream credit. The used-up credit blocks the
connect-accepted response on the control stream, so a late session
never finishes its handshake.

## Decision

The picoquic WebTransport server goes silent once four or more sessions
connect. A fresh bidirectional stream per reliable message uses up the
connection's stream credit. The used-up credit blocks the
connect-accepted response on the control stream, so a late session
never finishes its handshake. Reliable traffic now rides one
persistent bidirectional WebTransport stream per session. The client
opens the stream once, right after connect-accepted, and appends
length-prefixed frames to it for the life of the session. Each frame
header carries a channel number and a reliable bit, so the receiver
reads the channel straight from the frame. Unreliable traffic still
rides datagrams. This design matches the picoquic `wt_baton` reference
and the webtransportd frame spec. The stream count per session stays
at one, so concurrent joins keep their stream credit and reach the
open state.

## References

- Full drivers, considered options, supporting invariants, and the
  confirmation record: `DETAILS.md`
- Original record:
  `decisions/20260612-webtransport-persistent-framed-stream.md`
- Lean+Plausible proofs:
  [http3-queue](https://github.com/v-sekai-multiplayer-fabric/http3-queue)

## Related

- `rfd/0049-fabric-channels-as-reliability-classes`: the channel and
  reliability-class model this stream carries.
- `rfd/0052-http3-listener-session-findings`: other http3
  multi-session findings.

## Detail

{{< include DETAILS.md >}}
