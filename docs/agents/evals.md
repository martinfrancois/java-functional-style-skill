# Eval Guidance

## Scope

Use this when editing `evals/`, `evals-reference/`, `evals-regression/`, benchmark claims, or
scoring rules.

## Integrity Rules

- Don't cheat. Don't leak the diagnosis or desired fix in eval prompts.
- Natural activation prompts must not mention `$java-functional-style`, "use the skill", or similar
  command-style phrasing.
- Explicit invocation prompts may say `Use $java-functional-style`, but must set
  `metadata.invocation` to `explicit` and must not be reported as natural activation evidence.
- Runtime references must not contain eval inventories, expected outputs, score rubrics, hosted run
  IDs, private paths, private logs, or fixed score claims.
- Same-domain or near-solution overlap between runtime references and eval tasks is allowed only for
  explicitly classified focused or regression evidence, not ordinary broad lift.
- Metadata rationale documents why a classification is honest; free-form rationale text does not
  bypass validation.
- Every Java scenario task must state the Java version to assume.

## Categories

Every checklist item must use one of:

- `safety`
- `functional_style`
- `maintainability`

Main eval implementation scenarios need compile/artifact and behavior checks as safety checks, but
the public benchmark should be weighted toward `functional_style`.

## Evidence Types

Use `metadata.evidence_type` when scenario placement needs to be explicit:

- `ordinary_lift`: an ordinary main or reference scenario where both variants are fair to compare.
  Invalid in `evals-regression/`.
- `focused_main`: a main-suite scenario that intentionally covers a specific skill behavior and may
  share bounded, documented runtime-reference overlap. Report separately from ordinary broad lift.
- `focused_reference`: a reference-suite scenario that intentionally emphasizes a specific skill
  behavior or behavior delta. It may carry high weight on that focused behavior, but is not ordinary
  broad lift or unseen generalization evidence.
- `solved_regression`: a regression scenario that hosted history shows both variants solve at 100%.
  Invalid outside `evals-regression/`.
- `skill_context_dependent`: a regression scenario that requires exact skill-provided text,
  commands, procedures, checklists, headers, or bundled reference text. Invalid outside
  `evals-regression/`.

## Functional-Style Scenario Focus

Scenarios should cover:

- `Function.identity()` and `UnaryOperator.identity()` when required by the target API
- no-op identity stages that should be removed
- block or multi-line callbacks that should become named helpers
- supplier laziness
- checked IO, parser, and prompt boundaries
- side-effect callbacks
- cases where plain Java is clearer than forced functional style

Do not weaken, delete, move, or rewrite existing stream or Optional eval criteria to hide a
composition regression before the baseline-to-composed comparison has passed.

## Hosted Eval Use

- Run quality review first for runtime skill changes.
- If quality is below 100, fix quality before any hosted eval run.
- Run changed scenarios targeted before broad suites.
- If any targeted with-context result is below 100%, fix and rerun only the failed targeted
  scenarios.
- Broaden only after targeted runs are clean.
- With-context must be 100% for every retained functional-style scenario before package quality is
  claimed.
- If hosted evals are unavailable, document the blocker and exact remaining commands. Local
  validation alone is not enough for the composition quality gate.
