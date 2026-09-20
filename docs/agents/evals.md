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
region and changes over time (`tessl eval run --list-agents`). Before a release-readiness claim,
rerun the main suite with `--runs 2` or more, or with a stronger model such as
`--agent claude --model claude-sonnet-4-6`, and report both. A single run is not evidence of a
stable lift ratio.

## Composition

Runtime skill or rule changes must also pass the composition check in
[Ownership Boundaries](ownership-boundaries.md): the sibling skills' existing evals, unchanged,
run with both skills as context via `scripts/run_composed_eval.sh`. Never edit a sibling's evals to
make this pass.

## Current Suite Composition

Update this section whenever active eval membership or scoring changes.

- Main eval set: empty until the pending reruns below classify candidates.
- Reference suite: 6 candidate scenarios, 600 checklist points, 5 natural and 1 explicit.
- Regression suite: 8 solved scenarios, 800 checklist points, run with context only.
- Hosted evidence so far (Tessl default solver, 2026-09-20):
  - `01a0bf9d-d8ec-7269-a8d3-0c7d9986b4f1`: `07` isolated, without 20 / with 100, before the task
    fixed the carrier style; rerun pending.
  - `01a0bfa2-c49e-7178-a1a1-910db1b92785`: the other twelve candidates, both variants. Eight
    scored 100/100 in both arms and moved to regression; `04` (97/100) and `12` (99/100) stay in
    reference; `09` (20/85) and `13` (20/46) need reruns after the skill and criteria changes.
  - Quality review `01a0c029-facf-7109-8d99-7d4da1addc95`: 100.
- Pending before any score or lift claim: reruns of `07`, `09`, `13`, and the new `14` against
  the current skill bundle, classification, promotion, a main-suite run, and the composition
  checks.

## References

- [Workflow](workflow.md)
- [Skill Behavior](skill-behavior.md)
- [Pre-Submit Gate](pre-submit-gate.md)
- [Ownership Boundaries](ownership-boundaries.md)
