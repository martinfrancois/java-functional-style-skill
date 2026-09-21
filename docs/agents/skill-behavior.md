# Skill Behavior

Use this when editing `skills/java-functional-style/SKILL.md`, runtime references, rule text,
skill metadata, install instructions, or package behavior.

## Scope

`java-functional-style` owns general Java lambda and functional-interface style:

- lambdas and method references
- `Function.identity()` and `UnaryOperator.identity()`
- no-op functional stages
- callback readability and helper extraction
- supplier laziness
- side-effect boundaries in callbacks
- functional-interface Java baseline compatibility

It must not become a stream semantics skill or an Optional semantics skill.

## Behavior Rules

- Preserve behavior first: ordering, laziness, exceptions, null behavior, side effects, mutability,
  object identity where observable, and Java baseline compatibility.
- Prefer method references only when they are clearer and behavior-preserving.
- Use JDK identity functions only for truly identity callbacks required by the target API.
- Remove redundant identity stages when removing the stage preserves behavior.
- Extract helpers for block callbacks, temporary variables, branching, nested fluent chains, checked
  work, merge rules, formatting, or more than one meaningful condition.
- Keep supplier fallback work lazy.
- Keep plain branches or loops for checked IO, prompts, parser boundaries, complex early exits, or
  mutation-heavy code.
- Do not force streams, Optionals, or callback-heavy style where plain Java is clearer.

## Reference Policy

Runtime references must not contain eval inventories, expected outputs, score rubrics, hosted run
IDs, private paths, private logs, or non-public tokens.

Same-domain eval examples may exist only when eval metadata classifies them honestly as focused or
regression evidence.
