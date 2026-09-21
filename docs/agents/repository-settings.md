# Repository Settings

The GitHub repository mirrors the settings of `java-streams-skill`.

## Applied Settings

- Visibility: public
- Issues: enabled
- Wiki: disabled
- Projects: disabled
- Delete branch on merge: enabled
- Squash merge: enabled
- Rebase merge: enabled
- Merge commits: disabled
- Branch protection: none on `main`, matching the source repository at bootstrap time
- Actions permissions: enabled, all actions allowed
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

## Secrets

GitHub secrets are not readable and must not be copied.

Required secret:

- `TESSL_TOKEN` is required for authenticated Tessl review, dry-run publish, and real publish.

Real publish runs only through the release workflow. Runtime changes are not done until the
hosted checks and the composition check pass.
