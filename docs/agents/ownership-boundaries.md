# Ownership Boundaries

`java-functional-style` owns general Java lambda and functional-interface style: method
references, identity functions, no-op functional stages, callback readability and helper
extraction, supplier laziness, method-reference pitfalls, checked-exception boundaries in
callbacks, and callback side-effect boundaries.

`java-streams` owns stream and collector semantics. `java-optionals` owns Optional semantics.

Each package works on its own. This package must never depend on a sibling being installed, and
its guidance must not decide which stream operation, collector, or Optional method to use. When
both a domain skill and this package are active, the domain skill owns semantics and this package
only changes how callbacks are written.

Install the domain skill and this package together when you want both semantic guidance and
callback-style guidance.

## Composition Check

The sibling packages keep their released runtime text unchanged. What this package must prove is
that adding it does not make a sibling worse:

```text
java-streams alone (published)   <= java-streams + java-functional-style (with-context)
java-optionals alone (published) <= java-optionals + java-functional-style (with-context)
```

Run the check from local checkouts with the sibling evals unchanged:

```bash
scripts/run_composed_eval.sh ../java-streams-skill main
scripts/run_composed_eval.sh ../java-optionals-skill main
```

Every retained scenario must reach 100% with-context. Broaden to `reference` and `regression`
when budget allows and always after a change that touches review wording. Criterion-level
results must be equal or better at criterion level, not only in the total.

Run the check after any change to `skills/java-functional-style/` or `rules/`. If it regresses a
sibling, fix it here. Do not edit sibling evals, and do not copy sibling guidance into this
package to compensate.
