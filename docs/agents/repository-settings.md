# Repository Settings

The GitHub repository started from the settings of `java-streams-skill`. The lists below are this
repository's own settings; check them with `gh repo view` and
`gh api repos/martinfrancois/java-functional-style-skill/rulesets`.

## Applied Settings

- Visibility: public
- Issues: enabled
- Discussions: enabled
- Wiki: disabled
- Projects: disabled
- Delete branch on merge: enabled
- Squash merge: enabled
- Rebase merge: enabled
- Merge commits: disabled
- Branch protection: no classic protection rule; the ruleset below covers `main`
- Actions permissions: enabled, all actions allowed; "Allow GitHub Actions to create and approve
  pull requests" on, because Release Please opens its release PR with `GITHUB_TOKEN`
- Environment: `tessl-release`

Topics:

- `java`
- `lambdas`
- `functional-programming`
- `functional-interfaces`
- `method-references`
- `clean-code`
- `code-review`
- `refactoring`
- `tessl`
- `skills`
- `ai-coding`

## Ruleset On `main`

The active ruleset "Required merge checks" targets the default branch:

- Changes land through a pull request, merged by squash or rebase; zero approvals are needed, but
  every review thread must be resolved, and a new push dismisses stale approvals.
- Required status checks: `Validate skill and plugin` and `Commitlint`, both from GitHub Actions.
  The branch does not have to be up to date with `main` before merging. The CI job
  `Tessl publish dry-run` runs only on pushes to `main`, so it is not a pull request check. No
  check runs `tessl review run`.
- Linear history: no merge commits.
- No force pushes and no deletion of `main`.
- Bypass: the repository admin role can bypass every rule, for example with
  `gh pr merge --admin`.

## Secrets

GitHub secrets are not readable and must not be copied.

Required secret:

- `TESSL_TOKEN` is required for dry-run publish and real publish. No workflow runs
  `tessl review run`; run it by hand (see [Workflow](workflow.md)).

Real publish runs only through the release workflow. Runtime changes are not done until the
hosted checks and the composition check pass.
