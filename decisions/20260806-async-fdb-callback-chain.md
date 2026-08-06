---
title: Async FDB callback chain on the libh2o event loop
date: 2026-08-06
status: accepted
decision-makers: K. S. Ernest (iFire) Lee
tier: proof of concept
---

> Ported from [`weftspun/h2o-bench-tpcc`](https://github.com/weftspun/h2o-bench-tpcc)'s
> `rfd/0011-async-fdb-callback-chain.md` as part of the [zone-server-h2o](https://github.com/v-sekai-multiplayer-fabric/zone-server-h2o)
> consolidation — see that repo's README for current status. Content below is the
> original RFD, unmodified except for this header and stripping the old State line.

## Decision

Implement TPC-C transactions as async callback chains over FDB futures.
Each transaction step is a function that submits an FDB future and
registers a callback for when it resolves. The callback performs the
next step.

## Pattern

```
create_transaction
  -> get(district)        [async future]
    -> on_district_read   [callback: extract next_o_id]
      -> get(customer)    [async future]
        -> on_customer_read [callback: extract discount]
          -> get(stock[0]) [async future]
            -> on_stock_read [callback: update stock, next item]
              -> ... (loop for 5-15 items)
              -> set(oorder, new_order, order_line[], stock[])
              -> commit [async future]
                -> on_commit [callback: send HTTP response]
```

## Why async, not blocking

FDB's C API is callback-based by design. `fdb_future_set_callback()`
fires when the future resolves. Blocking with
`fdb_future_block_until_ready()` would stall the event loop thread.

In the actor-lite architecture (RFD 0005), the H2O network thread
dispatches work to worker threads via SPSC rings. If a worker blocks
on FDB, it can't process the next request from its ring.

## Error handling and retry

On any FDB error (conflict, timeout, etc.), call
`fdb_transaction_on_error(tr, err)`. This returns a future. When it
resolves, the transaction has been reset. The callback re-reads the
first key and restarts the chain.

The retry is transparent: the same `new_order_ctx_t` struct flows
through the chain, carrying the transaction parameters. On reset,
the read state is cleared and the chain restarts from step 1.

## Memory management

Each transaction allocates a context struct (`new_order_ctx_t`,
`payment_ctx_t`, etc.) on the heap. The context is freed in the final
callback (commit success or unrecoverable error). The FDB transaction
handle is destroyed in the same callback.

No reference counting needed: the callback chain is linear, each step
has exactly one outstanding future, and the context outlives all
callbacks.

## Limitations

- No batching across transactions: each HTTP request creates its
  own FDB transaction. Batching multiple requests into one transaction
  would improve throughput but violate TPC-C spec (each terminal
  executes one transaction at a time).
- Stack depth is bounded: the callback chain is finite (max 15 stock reads +
  writes + commit), so no stack overflow risk.
