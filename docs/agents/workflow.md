# Workflow

## Scope

Use this for day-to-day work in this repository: auth checks, validation, commits, pushes, and
release-readiness.

## Rules

- `.tessl-plugin/plugin.json` says `"private": false`; public is irreversible on the registry, so
  never flip it back by hand.
- Do not run a real Tessl publish by hand. Releases publish through
  `.github/workflows/publish-tessl.yml` when Release Please creates the tag.
- Do not claim lift, release-readiness, or composition safety without the hosted run IDs that
  back the claim. If Tessl hosted evals, authentication, or comparison tooling is unavailable,
  stop after local changes and report the blocker with the exact remaining commands.
- When a command fails because auth, login, workspace, or permission state appears missing,
  re-check after the user says they changed it.

## Local Validation

Before committing changes to the skill, rule, README, evals, package metadata, scripts, CI, or
agent docs, run:

```bash
python3 scripts/validate_skill.py skills/java-functional-style
python3 scripts/validate_eval_criteria.py evals evals-reference evals-regression
python3 scripts/test_validate_eval_criteria.py
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

Follow [Eval Guidance](evals.md) for suite rules and [Pre-Submit Gate](pre-submit-gate.md) for
the budget-aware order. In short:

1. Quality review at threshold 100 for any runtime skill, reference, or rule change. Fix quality
   before spending eval budget.
2. Targeted runs of changed or affected scenarios with `scripts/run_eval_suite.sh`, then the
   broader suites once targeted with-context results are 100%.
3. The composition check with `scripts/run_composed_eval.sh` against local checkouts of
   `java-streams-skill` and `java-optionals-skill` whenever the runtime skill or rule changed.

Do not rerun hosted evals because they look slow; poll the run ID with `tessl eval view`. Never
run unbounded loops around quota-consuming commands.

## Commits

Use Conventional Commits. Keep runtime skill changes, eval changes, CI changes, and docs changes in
separate commits where practical. Any change that can move hosted lift (skill text, rule text,
runtime references, active eval tasks or criteria, suite membership) goes in its own commit and is
labelled lift-sensitive in the PR summary with a revert strategy.

Examples:

- `feat(skill): add callback extraction guidance`
- `fix(skill): keep supplier fallbacks lazy`
- `test(evals): add identity mapper coverage`
- `docs: clarify ownership boundaries`

## Release

Release Please owns changelog and version changes. Do not edit `CHANGELOG.md`,
`.release-please-manifest.json`, `.tessl-plugin/plugin.json`, tags, or GitHub releases by hand
unless repairing release state with explicit maintainer direction.

Merging a releasable PR (`feat`, `fix`) into `main` makes Release Please open a release PR;
merging that PR creates the tag and GitHub release and dispatches the Tessl publish workflow,
which runs `tessl plugin publish`; Tessl then runs the main suite server-side and shows the score
on the registry. The publish workflow needs the `tessl-release` environment and the `TESSL_TOKEN`
secret, both already set.

The first release should be `0.1.0`. With no tag behind the manifest, Release Please would pick
its own initial version, so type `Release-As: 0.1.0` by hand into the body of the squash commit
that lands the package on `main` (the default squash body is the commit list; replace it). The
first changelog will also list the scaffold and Renovate commits already on `main`.

Runtime changes are not done until the hosted checks in [Eval Guidance](evals.md) and the
composition check in [Ownership Boundaries](ownership-boundaries.md) have passed.

## References

- [Project Identity](project-identity.md)
- [Ownership Boundaries](ownership-boundaries.md)
- [Eval Guidance](evals.md)
- [Public Metadata And OSS Readiness](public-metadata.md)
- [Repository Settings](repository-settings.md)
