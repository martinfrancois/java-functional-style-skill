# Agent Instructions

Java Functional Style is a private-for-now Tessl-compatible skill that helps AI coding agents write,
review, and refactor Java lambdas, method references, functional interfaces, identity functions,
suppliers, predicates, consumers, callbacks, and no-op functional stages without changing behavior.

Before starting any task, open [Workflow](docs/agents/workflow.md) and follow it.

When the user corrects wording, naming, scope, eval design, public metadata, or project policy, make
that correction durable in the relevant file under `docs/agents/`.

Runtime skill or rule changes are not done until the hosted checks in
[Eval Guidance](docs/agents/evals.md) and the composition check in
[Ownership Boundaries](docs/agents/ownership-boundaries.md) have passed.

## Maintenance

`AGENTS.md` is intentionally minimal. Don't add topic-specific guidance here. See
[Maintaining Agent Docs](docs/agents/maintaining-agent-docs.md).

## More Detailed Instructions

- [Workflow](docs/agents/workflow.md)
- [Project Identity](docs/agents/project-identity.md)
- [Ownership Boundaries](docs/agents/ownership-boundaries.md)
- [README Guidance](docs/agents/readme.md)
- [Skill Behavior](docs/agents/skill-behavior.md)
- [Eval Guidance](docs/agents/evals.md)
- [Public Metadata And OSS Readiness](docs/agents/public-metadata.md)
- [Repository Settings](docs/agents/repository-settings.md)
- [Maintaining Agent Docs](docs/agents/maintaining-agent-docs.md)
