---
title: "RFD 0028: Hexagonal core/ports/adapters as the component convention"
rfd: "0028"
state: published
scope: cross-language component architecture
---

## Problem

Components in the stack span several languages and run as separate
processes. Each component binds to hardware, a GPU, the network, or
an engine runtime. A shared monolith or one in-memory object model
cannot hold across these boundaries.

## Decision

Components in the stack span several languages, run as separate
processes, and each binds to hardware, a GPU, the network, or an
engine runtime. A shared monolith or one in-memory object model cannot
hold across those boundaries. Every component instead takes a uniform
`core/` + `ports/` + `adapters/` layout. `core/` holds dependency-free
domain logic, tested in isolation against fixtures. A port is a narrow
interface the core defines, labelled driving (input in) or driven
(output out), and by data flow as `*_source` or `*_sink`; a port stays
at the lowest common denominator every binding language can implement,
often a C-ABI struct of function pointers. Adapters implement ports
against the real world: a device, a socket, a recorded fixture for CI,
a renderer. Components compose by wiring one component's sink to
another's source, in-process directly or across a process boundary
over a shared wire protocol.

## References

- Full context, decision drivers, consequences, and the `sinew-mocap`
  worked example: `DETAILS.md`
- Original record:
  `decisions/20260610-hexagonal-core-ports-adapters.md`
- `sinew-mocap` repos: `driver`, `mount_drift`, `solve`, `viewer`,
  `vr_bridge`
