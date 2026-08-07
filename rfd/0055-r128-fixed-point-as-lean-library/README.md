---
title: "RFD 0055: r128 Q64.64 fixed-point as a Lean library for the cores"
rfd: "0055"
state: published
scope: fixed-point math library for the Lean kernel cores
---

## Decision

The deterministic cores need Q64.64 fixed-point math inside the Lean
kernels, which lower to SPIR-V through lean-slang. The engine already
vendors the C `r128` library (`thirdparty/misc/r128`), but the
kernels are authored in Lean. The team considered calling the vendored
C `r128` from the host only and keeping the kernels in floating
point, and reimplementing Q64.64 ad hoc inside each kernel. Both are
rejected: floating point in the kernels breaks determinism, and an
ad-hoc Q64.64 per kernel drifts. The project ports `r128` to a Lean
library that the cores import for their Q64.64 fixed-point math,
because one Lean implementation feeds every kernel and lowers to
SPIR-V over 64-bit integer pairs, while the vendored C
`thirdparty/misc/r128` stays the host reference the Lean library
matches. The cores share one fixed-point implementation, so the host
reference and the SPIR-V kernels agree bit-for-bit. A Plausible suite
checks the Lean `r128` against the vendored C `r128` for matching
results, and the lowered SPIR-V reproduces the same results.

## References

- Original record:
  `decisions/20260612-r128-fixed-point-as-lean-library.md`

## Related

- `rfd/0032-core-codegen-lean-slang`: the lean-slang lowering path
  this library's fixed-point ops travel.
- `rfd/0034-deterministic-cores-integer-seeded-rng`: the determinism
  doctrine this fixed-point library serves.
