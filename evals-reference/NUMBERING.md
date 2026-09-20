Reference scenarios are candidate functional-style coverage. Promote to `evals/` only after an
isolated hosted run with both variants, the classifier recommendation, and the 30 percentage-point
main promotion floor documented in `docs/agents/evals.md`. Numbers are kept when a scenario moves,
so gaps here are scenarios that live in `evals/` or `evals-regression/`.

- `04-keep-supplier-fallback-lazy`: supplier laziness review. Hosted run
  `01a0bfa2-c49e-7178-a1a1-910db1b92785`: without 97, with 100. Kept as reference; the delta is
  below the main floor.
- `07-library-loan-index`: identity value mapper and readable merge in new collector code. The
  first run (`01a0bf9d-d8ec-7269-a8d3-0c7d9986b4f1`, without 20, with 100) scored the baseline
  down for writing loops; after the task stated the collector carrier style the rerun
  (`01a0c02f-abf8-776d-8038-3ae700a5d1e1`) scored without 97, with 100. Kept as reference.
- `12-chess-pairing-method-reference-review`: method reference receiver binding review. Hosted
  run: without 99, with 100. Kept as reference.
- `13-volunteer-shift-ordering`: comparator composition replacing a block comparator lambda.
  Promoted and demoted on 2026-09-20; see `evals/NUMBERING.md` for the five baseline samples.

Promoted to `evals/` on 2026-09-20: `09-podcast-episode-digests`, `14-aquarium-feeding-ledger`,
`15-vineyard-harvest-summaries`. See `evals/NUMBERING.md`.
