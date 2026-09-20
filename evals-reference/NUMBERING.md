Reference scenarios are candidate functional-style coverage. Promote to `evals/` only after an
isolated hosted run with both variants, the classifier recommendation, and the 30 percentage-point
main promotion floor documented in `docs/agents/evals.md`. Numbers are kept when a scenario moves,
so gaps here are scenarios that live in `evals/` or `evals-regression/`.

- `04-keep-supplier-fallback-lazy`: supplier laziness review. Hosted run
  `01a0bfa2-c49e-7178-a1a1-910db1b92785`: without 97, with 100. Kept as reference; the delta is
  below the main floor.
- `07-library-loan-index`: identity value mapper and readable merge in new collector code. The
  first run (`01a0bf9d-d8ec-7269-a8d3-0c7d9986b4f1`, without 20, with 100) was rerun after the
  task fixed the carrier style, because the baseline had lost points for writing loops.
- `09-podcast-episode-digests`: named predicate and mapping helper in new pipeline code. First run
  without 20, with 85; the predicate criterion was relaxed to accept combined named predicates.
- `12-chess-pairing-method-reference-review`: method reference receiver binding review. Hosted
  run: without 99, with 100. Kept as reference.
- `13-volunteer-shift-ordering`: comparator composition replacing a block comparator lambda. First
  run without 20, with 46; the skill did not teach comparator composition and now does.
- `14-aquarium-feeding-ledger`: block lambdas in `Map.merge`, `computeIfAbsent`, and
  `CompletableFuture` callbacks in new code.
