# Contributing

Thanks for helping improve Java Functional Style.

**Coffee on me.** If you've had a pull request merged here and we meet in person, at a conference or
anywhere else, tell me your GitHub handle and I'll buy you a coffee or a drink. It's one per person,
however many pull requests you've made. It's a thank-you, not payment: the project doesn't pay for
contributions or offer bounties.

Keep changes focused, public-safe, and conventionally committed.

## Three Ways To Contribute

I want your time to go into pull requests that don't collide with someone else's work and that I
can accept. So every contribution takes one of these paths:

- **Small fix**: a bug fix, a typo, a docs improvement or a similar small change needs no issue.
  Open a pull request straight away. If an issue for it already exists, claim that issue first as
  described in [Solve An Issue](#solve-an-issue).
- **Existing issue**: claim it with `/take` and wait for the assignment before you open a pull
  request (see [Solve An Issue](#solve-an-issue)).
- **New feature**: start a thread in the
  [Ideas discussions](https://github.com/martinfrancois/java-functional-style-skill/discussions/categories/ideas).
  Once I approve the feature there, I open an issue for it, and you claim that issue with `/take`.
  Please don't open a pull request for a feature without an approved issue that is assigned to you.

## Solve An Issue

Browse the [open issues](https://github.com/martinfrancois/java-functional-style-skill/issues) to
find one that interests you. I add the `help wanted` label to issues where community contributions
are especially welcome and the `good first issue` label for tasks suited to new contributors.

Before you start on an issue, check that nobody is assigned to it and that no open pull request
already addresses it. The issue's **Development** section in the sidebar lists the linked pull
requests. Then claim it by commenting `/take` on a line of its own, and wait until you're assigned
before you open a pull request. If the issue has the `help wanted` or `good first issue` label,
nobody holds it and no open pull request addresses it, a bot assigns it to you right away;
otherwise it replies with the reason. Nobody can take an issue that someone else holds, and you can
hold up to 3 issues at a time (set in the [claim workflow](.github/workflows/claim-issue.yml)). For
issues without those labels, leave a comment asking if you can work on it and I'll get back to you.
If you ask in plain words on a labeled issue ("can I take this?"), the bot answers once and tells
you whether `/take` would work.

If you haven't opened a pull request for the issue 14 days after you were assigned (or after your
last comment there), the bot asks in the issue whether you're still working on it. Reply there or
open a pull request, a draft is fine; if neither happens within 7 days of that reminder, the bot
unassigns you so someone else can take the issue. Once you have an open or merged pull request for
the issue, there are no reminders. If your pull request is closed without merging, the 14 days
start again from that day. The [claim reminders workflow](.github/workflows/claim-reminders.yml)
sets both waiting times. If you stop working on an issue, say so in a comment so someone else can
take it.

A pull request that closes an issue its author doesn't hold, or one that another open pull request
already addresses, gets a comment and the `claim conflict` label.

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

Real Tessl publishes run only through the release workflow.

CI doesn't run `tessl review run`. Each run costs 10 Tessl credits, so run it by hand when the
skill text or its references change.

## Eval Integrity

Runtime skill text, references, and the rule must not contain answers to eval tasks: no helper
names, identifiers, or criterion phrasing from any scenario. New scenarios start in
`evals-reference/`, use fresh domains, can be screened locally first (`scripts/local_screen.sh`,
see `docs/agents/local-screening.md`), and move to `evals/` only after an isolated hosted run and
the classifier recommendation. See `docs/agents/evals.md`.

Runtime changes must also pass the composition check: the sibling skills' evals, unchanged, run
with both skills as context via `scripts/run_composed_eval.sh`. Never edit a sibling's evals to hide
a regression.

## Commit Style

Use Conventional Commits, such as:

- `feat(skill): add callback extraction guidance`
- `test(evals): add identity mapper coverage`
- `docs: clarify ownership boundaries`

Keep runtime skill changes, eval changes, CI changes, and docs changes in separate commits where
practical.
