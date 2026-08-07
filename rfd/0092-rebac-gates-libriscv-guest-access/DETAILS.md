## Status

Discussion only. No implementation exists yet. Nothing today calls
`check_expr`, `rebac_can_json`, or any `lean-rebac-core` predicate from
a `libriscv` host callback.

## What `godot-sandbox` documents today

`godot-sandbox` is the reference `libriscv`-Godot integration.
`libriscv` itself calls "pause and resume ... a first-class citizen"
in its own README, and documents an "optional execution timeout using
instruction counting". `godot-sandbox` exposes a `restrictions`
property. Setting it `true` blocks
all external access by default, then five independent callbacks each
grant a narrow exception:

- `set_class_allowed_callback(func(sandbox, name): ...)` — gates class
  instantiation. Checked with `is_allowed_class(name)`.
- `add_allowed_object(obj)` / `remove_allowed_object(obj)` /
  `clear_allowed_objects()`, plus `set_object_allowed_callback(func(sandbox,
obj): ...)` for anything not in the explicit list.
- `set_method_allowed_callback(func(sandbox, obj, method): ...)` —
  gates method calls.
- `set_property_allowed_callback(func(sandbox, obj, prop): ...)` —
  gates property reads/writes.
- `set_resource_allowed_callback(func(sandbox, path): ...)`, checked
  with `is_allowed_resource(path)` — gates resource loads.

Each callback returns a plain boolean, independently of the other
four. None of them shares a subject/object model, a delegation
concept, or an audit trail. One documented workaround for building a
real whitelist is to run once in trace mode. This logs every access
request a callback sees, then a person hand-promotes the log into a
static allow-list. This RFD's ReBAC model closes that gap
structurally, not by manual log review.

## The existing ReBAC engine this reuses

`thirdparty/taskweft-nif/standalone/tw_rebac.hpp` (in
`zone-server-h2o`, ported from `plan_memory/rebac.py`, no Godot
dependency) already implements:

- A relation vocabulary: `HAS_CAPABILITY`, `CONTROLS`, `OWNS`,
  `IS_MEMBER_OF`, `DELEGATED_TO`, `SUPERVISOR_OF`, `PARTNER_OF`, plus
  an `UNKNOWN`/string-named escape hatch for domain-specific relations.
- A boolean expression algebra over relations: `base`, `union`,
  `intersection`, `difference`, `tuple_to_userset` (Zanzibar's own
  "pivot through another relation" pattern) — `check_expr()`.
- `IS_MEMBER_OF` transitive inheritance and `CONTROLS`/`DELEGATED_TO`
  inversion, both handled inside `check_base()`, not bolted on per
  caller.
- `can()`/`rebac_can_json()` — a DFS capability search that returns
  the actual path, not just a boolean, format:
  `{"authorized":bool,"path":[...]}`. This is the audit trail
  `godot-sandbox`'s five callbacks do not have today.
- JSON (de)serialization (`graph_from_json`/`graph_to_json`), so a
  guest's capability graph is itself data, not code.

`lean-rebac-core`'s `ReBAC.lean`/`rebacCheck` (already referenced by
`zone-server-h2o`'s own `src/gen/rebac.c`, per `rfd/0083`) is the
Lean-proved version of the same idea — a pure predicate over
`Relation`/`Action` ranks, checked against proved theorems
(`rebac_empty_denied`, `rebac_public_observe`, the owner-only
`.modify` boundary). Either engine fits this design. Which one a real
implementation picks is a separate, later decision.

## Proposed mapping

| `godot-sandbox` axis         | ReBAC subject       | ReBAC object          | Relation                               |
| ---------------------------- | ------------------- | --------------------- | -------------------------------------- |
| Class instantiation          | the guest `Machine` | the class name        | `HAS_CAPABILITY`                       |
| Object access                | the guest `Machine` | the object instance   | `HAS_CAPABILITY` or `CONTROLS`         |
| Method call                  | the guest `Machine` | `<object>.<method>`   | `HAS_CAPABILITY`                       |
| Property access              | the guest `Machine` | `<object>.<property>` | `HAS_CAPABILITY`                       |
| Resource load                | the guest `Machine` | the resource path     | `HAS_CAPABILITY`                       |
| Instruction-budget extension | the guest `Machine` | the "more gas" action | `DELEGATED_TO` from a supervisor/owner |

Delegation, membership, and capability inheritance fall out of the
expression algebra already in `tw_rebac.hpp`. A guest that is
`IS_MEMBER_OF` a trusted group inherits that group's `HAS_CAPABILITY`
edges automatically, with no new code path per axis. `godot-sandbox`
needs a new hand-written callback for each such case today.

## Consequences

Good: one authorization model instead of five independent callbacks
plus a two-tier VM split. A denied check returns a real reason (no
path found), not just `false`. The engine is not new, untested code —
`tw_rebac.hpp` already has real callers in `taskweft-nif`, and
`lean-rebac-core`'s version is Lean-proved.

Bad: the team has not implemented this yet. `zone-guest-middleham`'s
`mud-sandbox-orchestrator` calls exactly two `vmcall`-reachable guest
functions today (`mud_boot`, `mud_step`). It has no host-capability
surface yet for this model to gate. The design has nothing to attach
to until that surface grows. No one wired
`thirdparty/taskweft-nif` into `zone-server-h2o` yet —
`mud/domains/README.md` already says the MUD guest does not use any
of its three domains yet. So reusing `tw_rebac.hpp` here means
depending on code that is itself not yet load-bearing anywhere.

## Revisit when

`zone-guest-middleham`'s guest surface grows past `mud_boot`/`mud_step`
into calling named host functions/classes/objects (the shape
`rfd/0079` left open). At that point, build the five-axis mapping
table above as real code, backed by either `tw_rebac.hpp` or
`lean-rebac-core`'s `rebacCheck`, instead of ad hoc per-axis callbacks.
