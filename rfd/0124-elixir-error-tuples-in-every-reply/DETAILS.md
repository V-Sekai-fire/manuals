## The subset that is written

The writer emits eight tags. Nothing else is needed for `:ok`, `{:ok, map}` and
`{:error, reason}`, and a smaller writer is a smaller thing to get wrong.

| tag | number | use |
| --- | --- | --- |
| `VERSION_MAGIC` | 131 | the first byte of every term |
| `SMALL_ATOM_UTF8_EXT` | 119 | an atom under 256 bytes |
| `ATOM_UTF8_EXT` | 118 | a longer atom |
| `SMALL_INTEGER_EXT` | 97 | 0 to 255 |
| `INTEGER_EXT` | 98 | a signed 32-bit integer |
| `BINARY_EXT` | 109 | an Elixir binary, which is what a string is |
| `SMALL_TUPLE_EXT` | 104 | a tuple with fewer than 256 elements |
| `MAP_EXT` | 116 | a map |

A reply that needs a larger integer, a float, a list or a reference is refused by the writer
rather than encoded. The refusal is the check: a reply shape nobody agreed on does not reach a
caller in a form that decodes.

## The test against a real virtual machine

Run on Erlang/OTP 29, 2026-08-17. The bytes came from the Python writer and went to `elixir`
with no intermediate step.

    decoded: {:error, {:res_below_minimum, %{got: 512, minimum: 1280}}}
    MATCHED {:error, {:res_below_minimum, %{got: 512, minimum: 1280}}}
    is_tuple: true  elem0_is_atom: true

The term is a tuple, its first element is an atom, and it matches the clause a caller writes.

## What `[:safe]` does, measured rather than assumed

The first run above decoded under `[:safe]` although `:res_below_minimum` is not an atom any
release ships. That looked like evidence that `[:safe]` permits new atoms. It is not. The test
script names the atom in its own `case` clause, so compiling the script created the atom before
the decode ran.

A second test used an atom that no module names:

    safe REFUSED it (ArgumentError) => :safe blocks novel atoms
    atom_count before=18541 after=18914
    without :safe: {:error, :zz_never_seen_atom_9f3a2b}

So `[:safe]` refuses an atom the virtual machine does not have, and a decode without it creates
one. Both halves are necessary to the decision: `[:safe]` is what stops a reply from growing the
atom table, and the caller's own clauses are what make the reasons it expects decodable.

This is recorded because the first reading was wrong and the wrong reading was the comfortable
one. A claim about a safety option that nobody runs is a claim that stays wrong.
