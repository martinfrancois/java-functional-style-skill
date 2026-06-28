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

## Composition Gate

Before opening any PR:

- Stream composition must prove:

  ```text
  current java-streams behavior <= slimmed java-streams + java-functional-style behavior
  ```

- Optional composition must prove the equivalent relationship if Optional runtime guidance or evals
  changed.
- Criterion-level results must be equal or better.
- Local validation alone is not enough.

## Evidence Cache

If scripts use local evidence caching, key it by the SHA-256 fingerprint of files under
`skills/java-functional-style/` and invalidate evidence when the skill bundle changes.
