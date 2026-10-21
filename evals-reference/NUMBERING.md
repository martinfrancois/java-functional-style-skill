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

## Rebuild by local baseline (2026-10-21)

Every scenario went through the local screen in `docs/agents/local-screening.md` (DeepSeek V4.1
Flash as the solver, a Claude Haiku judge; percentages, mean over the runs, range in brackets).
Not hosted evidence. The four prompts that named the skill became natural first, since no source
shows the maintainer naming it; `12` stays explicit as the one explicit scenario the two lift
suites need between them. The placement rule: baseline 98 to 100 in every run with the skill arm
at 98 or more is regression; baseline at least 30 under 100 with the skill arm at 100 is main;
everything else is reference.

| Scenario | Runs | Without skill | With skill (1.0.0 text) | Suite |
| --- | --- | --- | --- | --- |
| `01-to-map-function-identity-mapper` | 2 | 98 (97 to 99) | 99 (98 to 99) | reference |
| `02-remove-identity-map-stage` | 2 | 100 | 100 | regression |
| `03-extract-block-callback-helper` | 2 | 92 (84 to 100) | 100 | reference |
| `04-keep-supplier-fallback-lazy` (natural now) | 5 | 96 (87 to 99) | 99 (97 to 100) | reference |
| `05-checked-boundary-plain-branch` | 2 | 100 | 99 (99 to 100) | regression |
| `06-do-not-force-functional-style` | 2 | 99 (97 to 100) | 100 | reference, focused |
| `07-library-loan-index` | 5 | 71 (40 to 94) | 100 | reference, bimodal unaided |
| `08-track-name-normalizers` | 2 | 100 | 100 | regression |
| `09-podcast-episode-digests` | 2 | 21 (20 to 22) | 100 | main |
| `10-bike-station-fallbacks` (natural now) | 5 | 100 | 84 (68 to 99), judge noise on a plain branch | regression, rescreened below |
| `11-trail-permit-reader` | 2 | 100 | 100 (99 to 100) | regression |
| `12-chess-pairing-method-reference-review` (explicit) | 5 | 96 (94 to 98) | 99 (98 to 99) | reference |
| `13-volunteer-shift-ordering` | 5 | 80 (50 to 100) | 70 (50 to 90) | regression after the fix below |
| `14-aquarium-feeding-ledger` (natural now) | 5 | 40 (35 to 46) | 100 | main |
| `15-vineyard-harvest-summaries` | 2 | 35 | 100 | main |

`01`, `03`, and `06` left regression because one run of each dipped under 98 unaided.

`13` had two problems. Step 6 listed a tie-break rule as a reason to extract a helper, so the
solver wrote a comparator helper with an `if`/`else` chain; the comparator rule is now its own
step, and the rule file says the same. And the starting code returned 0 for two null leads
without comparing slots, while the checklist asked for slots ascending in every case, so a
correctly composed comparator changed the order. With the starting code comparing slots for null
leads too, the screen scored 100 in three runs of three in both arms, and `13` moved to
regression. `10` rescreened at 100 in three runs with the skill after an earlier 68 the local judge
had called a full pass in its own reasoning.
