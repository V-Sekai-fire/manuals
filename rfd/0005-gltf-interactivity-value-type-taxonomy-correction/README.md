---
title: "RFD 0005: gltf_interactivity's value types: primitive, ref, and custom"
state: discussion
scope: zone-server-h2o CastSpell
---

## Decision

`gltf_interactivity`'s vendored specification defines three value-type
categories, not the two-way primitive/`ref` split `RFD 0001` item 5
first described: primitive types (`bool`, `float`, the `float2`/`3`/`4`
vectors and matrices, `int`), `ref` (an opaque reference, null by
default), and `custom` (a signature that defers all type semantics to
an extension). `zone-server-h2o` implements only the first two today;
CastSpell's bitpacked struct gives a primitive field its value inline
and a `ref` field a slotmap handle. Leave `custom` unimplemented, not
rejected, until a CastSpell parameter needs an extension-defined type.

## References

- Full taxonomy detail and verification: `DETAILS.md`
- `taskweft/thirdparty/gltf_interactivity/01_core_concepts.md`,
  `03_extending_gltf.md`

## Related

`rfd/0001-zonefabric-roadmap-vs-mas-bandwidth-fps/README.md` (item 5),
`rfd/0003-castspell-sandbox-package-and-manifest-encoding/README.md`
