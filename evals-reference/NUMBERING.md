Reference scenarios are candidate functional-style coverage. Promote to `evals/` only after an
isolated hosted run with both variants, the classifier recommendation, and the 30 percentage-point
main promotion floor documented in `docs/agents/evals.md`. Numbers are kept when a scenario moves,
so gaps here are scenarios that live in `evals/` or `evals-regression/`.

- `04-keep-supplier-fallback-lazy`: supplier laziness review. Run
  `01a0bfa2-c49e-7178-a1a1-910db1b92785`: without 97, with 100; with-context again 100 against the
  final bundle in `01a0c1de-dc0a-7653-990c-5b345cd0bcc3`. Focused reference coverage; it
  shares the lazy-fallback shape with the runtime example and the delta is below the main floor.
- `07-library-loan-index`: identity value mapper and readable merge in new collector code. The
  first run (`01a0bf9d-d8ec-7269-a8d3-0c7d9986b4f1`, without 20, with 100) scored the baseline
  down for writing loops; after the task stated the collector carrier style the rerun
  (`01a0c02f-abf8-776d-8038-3ae700a5d1e1`) scored without 97, with 100. Kept as reference.
- `12-chess-pairing-method-reference-review`: method reference receiver binding review. Run
  `01a0bfa2-c49e-7178-a1a1-910db1b92785`: without 99, with 100; with-context again 100 against the
  final bundle in `01a0c1de-dc0a-7653-990c-5b345cd0bcc3`. Kept as reference.
- `13-volunteer-shift-ordering`: comparator composition replacing a block comparator lambda.
  Promoted and demoted on 2026-09-20; the main-suite notes list the six baseline samples. The
  runtime comparator example shares its shape, so it is focused reference coverage.

Promoted to `evals/` on 2026-09-20: `09-podcast-episode-digests`, `14-aquarium-feeding-ledger`,
`15-vineyard-harvest-summaries`. See `evals/NUMBERING.md`.

With-context run against the PR #18 runtime text on 2026-10-03 (default solver
`deepseek-v4.1-flash`), `01a1039d-6446-715f-b116-ce90aa5fe99d`: `04` 100, `07` 100, `12` 99 (a
review aside about synchronization), `13` 71 (the solver moved the tie-break into a helper with an
`if`/`else` chain instead of `thenComparingInt`). Isolated reruns: `12` 100 in
`01a103ae-6281-76c5-8f81-6e58d91e2dc6`, `13` 100 in `01a103a7-5363-77f9-8b8b-8a8fe9cf428f`. Watch
`13` if the with-context miss repeats; step 6 of the skill lists a tie-break rule as a reason to
extract a helper, which pulls against the comparator composition sentence below it.
