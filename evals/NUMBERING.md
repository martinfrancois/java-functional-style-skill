Main scenarios keep the number they had in `evals-reference/`, so gaps are scenarios that live in
`evals-reference/` or `evals-regression/`. Promotion follows `docs/agents/evals.md`: an isolated
hosted run with both variants, a clean with-context result, and a delta of at least 30 percentage
points.

Promoted on 2026-09-20 (Tessl default solver):

- `09-podcast-episode-digests`: run `01a0c02f-abf8-776d-8038-3ae700a5d1e1`, without 20, with 100.
  Covers helper extraction and named predicates in a stream pipeline.
- `13-volunteer-shift-ordering`: run `01a0c02b-3822-71db-aef0-e746e472e5b7`, without 50, with 100.
  Covers comparator composition replacing a block comparator lambda.
- `14-aquarium-feeding-ledger`: natural run `01a0c02f-abf8-776d-8038-3ae700a5d1e1`, without 30,
  with 100; explicit-invocation run `01a0c037-590b-7193-ab1e-9558506ca102` (current text), without
  44, with 100. Covers block lambdas in `Map.merge`, `computeIfAbsent`, and `CompletableFuture`
  callbacks.
- `15-vineyard-harvest-summaries`: run `01a0c077-0e44-773d-b1cb-ab99ef402216`, without 35, with
  100. Covers block lambdas in `Optional.map`, a `groupingBy` downstream, and label formatting.

Variance note: in the full main-suite run `01a0c04c-f644-72ed-8e3a-d53d3f8e3d06` the baseline
solved `13` at 100/100 (earlier samples 20 and 50). The default solver sometimes composes
comparators on its own, so `13` is the least stable delta in the suite; it stays because its mean
delta across samples is above the floor and it covers a callback shape no other scenario has.

`09`, `13`, and `15` are natural-activation implementation tasks; `14` invokes the skill explicitly so the main suite keeps both styles (explicit run above). Identity-function, supplier-laziness,
checked-boundary, and method-reference scenarios did not clear the floor because the default
solver already handles them; they remain as reference or regression coverage.
