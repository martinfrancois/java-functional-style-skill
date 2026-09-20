# Pre-Submit Gate

## Scope

This page captures the internal pre-submission procedure for skill and eval changes.

## Rules

- Run `tessl review run --workspace martinfrancois --threshold 100 skills/java-functional-style/SKILL.md`
  first for runtime skill or reference changes. If this fails, stop and fix quality.
- Run local validation before hosted evals:

  ```bash
  python3 scripts/validate_skill.py skills/java-functional-style
  python3 scripts/validate_eval_criteria.py evals evals-reference evals-regression
  python3 -m py_compile scripts/*.py
  bash -n scripts/*.sh
  python3 scripts/validate_json_files.py
  python3 scripts/validate_openai_agent_yaml.py
  tessl plugin lint .
  ```

- Start hosted evals with targeted affected scenarios.
- If a targeted with-context result is below 100%, fix it and rerun only the failing scenario.
- Broaden only after targeted checks are clean.
- Do not rerun hosted evals because they appear slow or missing scoring. Wait patiently for Tessl to
  complete scoring or return a hard service failure.
- Never use unbounded loops for hosted evals, reviews, or other quota-consuming commands.
- If unexpected background work appears, audit process ancestry and Codex session logs before
  explaining the cause.
- If Tessl eval access is blocked, stop and record exact blocked commands.

## Composition Check

After the functional-style suites are clean for the final skill bundle, run the composition check
from [Ownership Boundaries](ownership-boundaries.md) with `scripts/run_composed_eval.sh` against
local checkouts of the sibling repositories. Every sibling scenario must stay at 100%
with-context; criterion-level results must be equal or better.
