## Status

Discussion only. Nobody wrote a compiler, and nobody proved the two
hard constructs below stay regular. That proof decides whether this
RFD is buildable at all.

## What backtracks today

`tw_rebac.hpp` carries two evaluators, and both backtrack.

`check_expr` walks the expression tree by recursive descent. It
decrements `p_fuel` at each `union`, `intersection`, `difference`, and
`tuple_to_userset` node, and it returns `false` when fuel reaches
zero. `check_base` recurses the same way through an `IS_MEMBER_OF`
chain.

`_rebac_dfs` searches depth-first for a capability path. It copies its
visited set at every branch:

```
std::vector<std::string> sub_path;
std::unordered_set<std::string> sub_visited = p_visited;
if (_rebac_dfs(p_g, e.object, p_target, sub_visited, sub_path, p_depth - 1)) {
```

Each element of that set is a heap-allocated string, so each branch
allocates.

Two hot paths call this work. `tw_domain.hpp`'s own goal-satisfaction
comment records the first. A goal binding whose `var` is a JSON object
gets:

```
parsed as a full RelationExpr (union, intersection, difference,
tuple_to_userset, …) and evaluated via check_expr.
```

The planner therefore calls `check_expr` per binding, per candidate
state, while it backtracks. `rfd/0092` adds the second: the same
evaluator in front of a `libriscv` guest host call, whose own cost is
3ns.

## What `re2` does instead

`re2` refuses to backtrack. It compiles a pattern to a program, then
simulates that program so every input position advances exactly once.
Its guarantee is linear time in input length, with bounded memory, and
no catastrophic blowup on an adversarial pattern. It builds the
deterministic automaton lazily, and when the state cache fills, it
flushes the cache rather than growing without limit.

The same three moves apply here:

1. **Compile once.** A named definition in `TwReBACGraph::definitions`
   compiles to an automaton over relation labels, by a Thompson
   construction. `union` becomes an alternation. Concatenation comes
   from `tuple_to_userset`'s pivot. `IS_MEMBER_OF` inheritance becomes
   a Kleene star on that one label.
2. **Simulate, do not search.** Evaluation runs the product of
   automaton state and graph node. States times edges bounds the work.
   Nothing copies a visited set, because the product state *is* the
   visited marker.
3. **Bound the cache.** Hold the lazy deterministic states in a fixed
   budget, and flush when full.

`p_fuel` then disappears. It exists only because a backtracking search
has no natural bound. A product simulation terminates because the
product state space is finite.

## This is not a stretch: relation expressions are path queries

A ReBAC relation expression describes a set of label paths from a
subject to an object. That is a regular path query, the same object
graph databases already evaluate. Zanzibar's userset rewrite rules
describe a restricted regular path language for the same reason. The
`base` case is a single label. `IS_MEMBER_OF` inheritance is that
label starred. So most of `check_expr` already denotes a regular
language, and a compiler for it is a translation, not an invention.

## The two constructs that resist

**`difference` needs complement.** Complement needs a deterministic
automaton, and determinization is worst-case exponential in the number
of states. `re2` lives with the same fact and answers it with a lazy
deterministic automaton plus a flushable cache. The same answer
applies here.

The sharper problem is not cost. It is monotonicity. `rfd/0092` states
an append-only monotonicity theorem: adding an edge never turns a
grant into a denial. That property is what makes a resolved capability
table safe to cache. **`difference` breaks that theorem.**

An expression of the form "A and not B" turns a grant into a denial as
soon as an edge satisfies B. So the two RFDs conflict, and the
conflict needs an explicit resolution, one of:

- Restrict `difference` out of any expression the enforcement path
  uses, and keep it for planning goals only.
- Keep `difference` and drop the caching theorem, which returns the
  hot-path cost problem `rfd/0092` open question 7 records.
- Prove a weaker, stratified monotonicity that holds for a negation
  depth of one.

This RFD does not pick one. It records that somebody must.

**`tuple_to_userset` moves the object.** A plain regular path query
fixes its target and varies the path. `tuple_to_userset` pivots
through one relation and then evaluates an inner expression against a
*different* subject, as `check_expr` shows:

```
for (size_t idx : sit->second) {
    const TwEdge &e = p_g.edges[idx];
    if (e.rel == pivot) {
        if (check_expr(p_g, e.object, iit->second, p_obj, p_fuel - 1)) {
```

Whether that stays regular is the open question that decides this
whole design. Nobody checked it. If it does stay regular, the product
construction above holds as written. If it does not, this RFD needs a
pushdown model or a restriction on nesting depth, and the linear-time
claim weakens accordingly.

## Verification this needs

`taskweft` already sets the precedent for proving a fast path equal to
a slow path. `tw_rebac.hpp`'s own comment on the `member_edges` index
reads:

```
Formally justified by Planner.ExpandIndex: expand_index_equiv proves
that iterating member_edges gives the same result as scanning all
edges.
```

The same obligation applies, at a larger scale:

- **Compilation equivalence.** The compiled automaton accepts exactly
  the subject and object pairs `check_expr` grants. This is
  `rfd/0092`'s resolution-equivalence theorem, and this RFD supplies
  its mechanism.
- **Termination without fuel.** The product simulation halts on every
  input, with no fuel parameter.
- **A cache flush changes no answer.** Flushing lazy deterministic
  states affects speed only, never a grant or a denial.
- **Differential test.** Run the compiled evaluator and the existing
  `check_expr` against the same graphs, and compare every answer, in
  the same shape `test/unit/test_xr_grid_entity_packet.c` compares a
  generated codec against golden vectors.

## Consequences

Good: one mechanism closes `rfd/0092`'s open question 4 (fuel has no
owner) and open question 7 (cost on the 64 Hz path). The fuel
parameter stops being a silent denial source. Planning and access
control share one evaluator, because both already call `check_expr`.

Bad: this is a compiler, and nobody wrote it. The `difference`
monotonicity conflict above is real and unresolved, and it touches an
already-merged RFD. Nobody answered the `tuple_to_userset` regularity
question, and a negative answer weakens the central claim. None of
this work has a caller yet, because `thirdparty/taskweft-nif` is not
wired into `zone-server-h2o`, and `rfd/0092`'s guest surface does not
exist either.

## Revisit when

Somebody answers the `tuple_to_userset` regularity question. That
answer decides whether to build the product construction as written,
or to fall back to a pushdown model with a bounded nesting depth.
Resolve the `difference` monotonicity conflict with `rfd/0092` in the
same pass, because the two answers together decide whether a resolved
capability table stays cacheable.
