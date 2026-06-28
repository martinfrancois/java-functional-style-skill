# Ownership Boundaries

`java-functional-style` owns general Java lambda and functional-interface style.

`java-streams` owns stream and collector semantics.

`java-optionals` owns Optional semantics.

Install the domain skill and this package together when you want both semantic guidance and
callback-style guidance.

## Composition Quality Gate

Do not open a PR, draft PR, or recommend merging until the composed setup has empirically proven
equal or better quality than the current baseline.

For streams:

```text
current java-streams behavior <= slimmed java-streams + java-functional-style behavior
```

For optionals, if optional runtime guidance or evals are changed:

```text
current java-optionals behavior <= slimmed java-optionals + java-functional-style behavior
```

The proof must use the existing evals before any criteria are rewritten, moved, weakened, or
deleted. Criterion-level results must be equal or better, not just total scores.

If hosted eval infrastructure, Tessl authentication, or comparison tooling is unavailable, stop
after local changes and report the blocker. Local validation alone does not satisfy this gate.

Do not solve regressions by copying all generic lambda guidance back into the domain skills. Add
only the smallest bridge text if evidence proves it is needed.
