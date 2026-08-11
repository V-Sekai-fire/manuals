---
title: "RFD 0112: Lexical for the slash command interface"
rfd: "0112"
state: published
scope: the Queen of the Gyre, and what serves her
---

## Problem

`fabric-store-domain/src/queen.c` has no client. Its `main()` founds a ward, runs the
cycles, prints, and exits, with no socket and no instance that outlives the run. A slash
command interface needs a live game and a field to type into, and neither exists.

The field is the harder half. When a player types `/commission`, it must show the parameter
as an inline block that the player cannot edit, with editable space around it. An HTML form
control holds plain text only. A `contenteditable` element can show a block, and written by
hand it fails on the caret, on mobile autocorrect, on IME composition, and on paste.

## Decision

Use Lexical, from Meta. Its decorator node is one block to the caret, which therefore
crosses a parameter in one key press, and Meta tests the mobile and IME paths at Facebook
scale. ProseMirror is rejected, because its atom node can hold the caret and needs a plugin
to correct it. The cost is developer speed, so the version is pinned.

The Queen's rows are entities and they take coordinates. A Spark, a venue, and a contract
each become an entity in the zone model, so the interest filter in `fabric-fanout-edge`
decides who sees a change. A Spark moving to a contract is local by intent and reaches every
box it enters. `/restart` reaches everyone, because one ward serves all players.

The ward is served the way a stream is served. One primary holds the fence and writes.
Secondaries read the same pages out of FoundationDB, and one is hosted when the primary
goes, which `check_fence` makes safe by refusing the old writer. A player may hold a
secondary as a fallback, and a background tab holds its seat with a keepalive.

The menu shows a command only when the caller's rebac relations permit it. The server checks
again on receipt. `fabric-asset-edge` serves the built client on Fly as a transport layer,
and `queen` gains a transport layer of its own.

## References

- Lexical: <https://lexical.dev>. ProseMirror: <https://prosemirror.net>
- RFD 0111 sets the words transport layer and service. RFD 0085 holds the setting.
- RFD 0049 holds the channel classes the ward scalars need. RFD 0050 sets the keepalive.
- The comparison, the entity mapping, and three hazards: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
