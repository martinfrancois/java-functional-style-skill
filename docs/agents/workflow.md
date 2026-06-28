# Workflow

## Scope

Use this for day-to-day work in this repository: auth checks, validation, commits, pushes, and
release-readiness.

## Rules

- Keep the GitHub repository private until François explicitly asks to make it public.
- Keep `.tessl-plugin/plugin.json` public-ready with `"private": true`.
- Do not run a real Tessl publish unless François explicitly asks.
- Do not open a PR, draft PR, or recommend merging until the composition quality gate in
  [Ownership Boundaries](ownership-boundaries.md) has passed.
- If Tessl hosted evals, Tessl authentication, or comparison tooling is unavailable, stop after
  local changes and report the blocker.
- When a command fails because auth, login, workspace, or permission state appears missing,
  re-check after the user says they changed it.

## Local Validation

Before committing changes to the skill, README, evals, package metadata, scripts, CI, or agent docs,
run the relevant local checks:

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

If `tessl plugin publish --dry-run .` fails only because the current manifest version already
exists, record that as expected for ordinary non-release changes and rely on the patch-bump dry-run.

## Hosted Evals

- Run quality review first for runtime skill or reference changes.
- If quality is below 100, stop and fix it before hosted evals.
- Start with targeted changed or affected scenarios.
- Broaden only after targeted with-context results are 100%.
- Do not rerun hosted evals just because they appear slow; wait for completed scoring or a hard
  service failure.
- Never run unbounded loops around hosted evals, reviews, or other quota-consuming commands.
- If unexpected background eval/review work appears, audit process ancestry and Codex session logs
  before explaining the cause.

## Commits

Use Conventional Commits. Keep runtime skill changes, eval changes, CI changes, and docs changes in
separate commits where practical.

Examples:

- `feat(skill): add callback extraction guidance`
- `test(evals): add identity mapper coverage`
- `docs: clarify ownership boundaries`

## Release

Release Please owns changelog and version changes. Do not edit `CHANGELOG.md`,
`.release-please-manifest.json`, `.tessl-plugin/plugin.json`, tags, or GitHub releases by hand
unless repairing release state with explicit maintainer direction.

Real Tessl publish is forbidden until François explicitly asks.

## References

- [Project Identity](project-identity.md)
- [Ownership Boundaries](ownership-boundaries.md)
- [Eval Guidance](evals.md)
- [Public Metadata And OSS Readiness](public-metadata.md)
- [Repository Settings](repository-settings.md)
