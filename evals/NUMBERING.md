Main scenarios keep the number they had in `evals-reference/`, so gaps are scenarios that live in
`evals-reference/` or `evals-regression/`. Promotion follows `docs/agents/evals.md`: an isolated
hosted run with both variants, a clean with-context result, and a delta of at least 30 percentage
points.

Promoted on 2026-09-20 (Tessl default solver):

- `09-podcast-episode-digests`: run `01a0c02f-abf8-776d-8038-3ae700a5d1e1`, without 20, with 100.
  Covers helper extraction and named predicates in a stream pipeline.
- `14-aquarium-feeding-ledger`: natural run `01a0c02f-abf8-776d-8038-3ae700a5d1e1`, without 30,
  with 100; explicit-invocation run `01a0c037-590b-7193-ab1e-9558506ca102` (current text), without
  44, with 100. Covers block lambdas in `Map.merge`, `computeIfAbsent`, and `CompletableFuture`
  callbacks.
- `15-vineyard-harvest-summaries`: run `01a0c077-0e44-773d-b1cb-ab99ef402216`, without 35, with
  100. Covers block lambdas in `Optional.map`, a `groupingBy` downstream, and label formatting.

Demoted the same day: `13-volunteer-shift-ordering` (comparator composition). Its with-context
result is 100 in every sample, but the default solver's baseline came in at 20, 50, 100, 84, and
100 across runs `01a0bfa2-c49e-7178-a1a1-910db1b92785`, `01a0c02b-3822-71db-aef0-e746e472e5b7`,
`01a0c04c-f644-72ed-8e3a-d53d3f8e3d06`, `01a0c077-e577-704b-ad68-9b7386d95575`, and `01a0c083-1918-704b-a748-8f26c39ad294`. The mean delta is
under the 30 pp floor, so it is reference coverage.

`09` and `15` are natural-activation implementation tasks; `14` invokes the skill explicitly so the main suite keeps both styles (explicit run above). Identity-function, supplier-laziness,
checked-boundary, and method-reference scenarios did not clear the floor because the default
solver already handles them; they remain as reference or regression coverage.
