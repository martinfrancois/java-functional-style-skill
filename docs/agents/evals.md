# Eval Guidance

## Scope

Use this when editing `evals/`, `evals-reference/`, `evals-regression/`, benchmark claims, or
scoring rules.

## Integrity Rules

- Don't cheat. Don't leak the diagnosis or desired fix in eval prompts.
- Runtime skill text, runtime references, and the rule must not contain eval inventories, expected
  outputs, score rubrics, hosted run IDs, private paths, fixed score claims, or the helper names,
  identifiers, and phrasing of any eval task or criterion. `validate_eval_criteria.py` flags shared
  domain identifiers between tasks and runtime references; Java keywords and the functional APIs
  this skill is about are excluded because sharing them is inherent.
- Natural activation prompts must not mention `$java-functional-style`, "use the skill", or
  similar command-style phrasing. Explicit invocation prompts may say
  `Use $java-functional-style`, must set `metadata.invocation` to `explicit`, and are not natural
  activation evidence.
- Every Java scenario task states the Java version to assume.
- Every scenario directory contains `task.md`, `criteria.json`, and `capability.txt`. Review-only
  tasks still require a concrete artifact such as `review.md`.
- Use domains that no runtime example and no sibling-skill eval uses. Stream and Optional
  scenarios live in their own repositories; a functional-style scenario may use a stream or an
  Optional as the callback carrier, but its criteria score the callback, not the stream or
  Optional choice.
- Every retained scenario must have a 100% with-context result against the current runtime bundle
  (`skills/java-functional-style/` plus `rules/`). Any commit that touches either directory
  invalidates that evidence for every suite, so freeze runtime text before spending hosted budget.

## Categories And Weighting

Every checklist item uses one of `safety`, `functional_style`, or `maintainability`.

Normalize ordinary 100-point scenarios around 15 safety, 80 functional-style, and 5
maintainability points unless a scenario documents a reason to differ. Safety items cover the
requested artifact, Java baseline, and behavior preservation; functional-style items carry the
lift.

## Evidence Types

`metadata.evidence_type` states how a scenario may be reported:

- `ordinary_lift`: both variants are fair to compare and the task shares no domain identifiers
  with runtime references. Valid in `evals/` and `evals-reference/`. This is the default for new
  scenarios.
- `focused_main` / `focused_reference`: intentionally overlapping coverage of one behavior,
  reported separately from broad lift and never as generalization evidence. Requires
  `metadata.runtime_reference_overlap_rationale`.
- `solved_regression`: hosted history shows both variants at 100. Only in `evals-regression/`.
- `skill_context_dependent`: needs exact skill-provided text or commands. Only in
  `evals-regression/`.

## Suites

- `evals/` is the main eval set used for the public lift score.
- `evals-reference/` holds candidates, diagnostics, and broad coverage.
- `evals-regression/` holds solved and skill-context-dependent coverage; run with context only.

## Classification And Promotion

1. Draft new scenarios in `evals-reference/` (or `evals-regression/` when skill-context
   dependent).
2. Run them in isolation with both variants: `scripts/run_eval_suite.sh reference <scenario>`.
3. Save `tessl eval view <run-id> --json` and run
   `scripts/classify_eval_result.py <run-json> --scenario-dir <scenario-dir>`.
4. Follow the classifier: with-context below 100 means fix first; both variants at 100 means
   regression; clean with-context plus a without-context gap means reference or main.
5. Main promotion floor: at least 30 percentage points of with-minus-without delta on the
   isolated run, plus new capability coverage. Do not promote weak-delta scenarios to make the
   suite look balanced, and do not suppress legitimate coverage to inflate lift.
6. Every retained scenario in every suite must have a 100% with-context result against the
   current skill bundle before it is reported.

## Model And Variance

Use the Tessl default solver unless intentionally comparing. The default model depends on the
region and changes over time (`tessl eval run --list-agents`). A single run is not evidence of a
stable lift ratio: before a release-readiness claim, every main scenario needs at least three
baseline samples against the current bundle, from `--runs` or from repeated runs, and the numbering
notes must list them. Use a stronger model (`--agent claude --model claude-sonnet-4-6`) as a
further sample when the plan allows model selection.

## Composition

Runtime skill or rule changes must also pass the composition check in
[Ownership Boundaries](ownership-boundaries.md): the sibling skills' existing evals, unchanged,
run with both skills as context via `scripts/run_composed_eval.sh`. Never edit a sibling's evals to
make this pass.

## Current Suite Composition

Update this section whenever active eval membership or scoring changes. Run IDs and per-run
numbers live in `evals/NUMBERING.md`, `evals-reference/NUMBERING.md`,
`evals-regression/NUMBERING.md`, and each scenario's `criteria.json` metadata, never here.

- Main eval set: 3 scenarios, 300 checklist points, 2 natural and 1 explicit, all implementation
  tasks: `09` helper extraction and named predicates in a pipeline, `14` `Map.merge`,
  `computeIfAbsent`, and `CompletableFuture` callbacks (explicit invocation), `15` `Optional.map`
  and collector-downstream callbacks. Each carries 80 functional-style points, 15 safety, 5
  maintainability. No weight multipliers.
- Reference suite: 4 scenarios, 400 points. `07` identity mappers and `12` method-reference
  receiver binding are ordinary coverage with a baseline near 100. `04` supplier laziness and
  `13` comparator composition are focused reference coverage because they share a shape with a
  runtime example; `13` also has an unstable baseline.
- Regression suite: 8 solved scenarios, 800 points, run with context only. Five of them keep the
  weighting of the package's first draft; their metadata says why.
- The public score measures the main suite only: callback extraction in pipelines, merge and
  completion callbacks, and Optional and collector-downstream callbacks. Identity functions,
  supplier laziness, checked boundaries, and method-reference reviews are regression or reference
  coverage because the default solver already handles them; say so wherever the score is quoted.
- Model selection is a paid-plan feature, so no stronger-model check exists. Sandbox cells drop at
  random on the free plan; `tessl eval retry <run>` creates a new run that reuses the completed
  cells.

## References

- [Workflow](workflow.md)
- [Skill Behavior](skill-behavior.md)
- [Pre-Submit Gate](pre-submit-gate.md)
- [Ownership Boundaries](ownership-boundaries.md)
