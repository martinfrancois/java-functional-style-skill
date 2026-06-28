# Contributing

Thanks for helping improve Java Functional Style.

This repository is private for now but should stay open-source-ready. Keep changes focused,
public-safe, and conventionally committed.

## Project Layout

```text
.
├── rules/
│   └── java-functional-style.md
├── skills/java-functional-style/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── functional-style-examples.md
│       ├── hard-stops.md
│       └── java-functional-api.md
├── evals/
├── evals-reference/
├── evals-regression/
└── scripts/
```

## Local Validation

Run the local checks relevant to your change:

```bash
python3 scripts/validate_skill.py skills/java-functional-style
python3 scripts/validate_eval_criteria.py evals evals-reference evals-regression
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh
python3 scripts/validate_json_files.py
python3 scripts/validate_openai_agent_yaml.py
tessl plugin lint .
```

Authenticated checks:

```bash
tessl review run --workspace martinfrancois --threshold 100 skills/java-functional-style/SKILL.md
bash scripts/check_publish_dry_run.sh .
tessl plugin publish --dry-run --bump patch .
tessl plugin publish --dry-run .
```

Do not run a real Tessl publish unless François explicitly asks.

## Eval Integrity

Do not rewrite, delete, weaken, or move existing stream or Optional eval criteria to hide a
composition regression. Before PRs are opened, the composed setup must prove equal or better than
the current domain-skill baselines on existing evals.

## Commit Style

Use Conventional Commits, such as:

- `feat(skill): add callback extraction guidance`
- `test(evals): add identity mapper coverage`
- `docs: clarify ownership boundaries`

Keep runtime skill changes, eval changes, CI changes, and docs changes in separate commits where
practical.
