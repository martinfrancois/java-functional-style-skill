# Java Functional Style Skill for AI Agents

Java functional-style code is easy to make plausible and hard to keep honest. A callback can hide a
contract change, a no-op `map` can survive a cleanup, an eager fallback can defeat laziness, and a
block lambda can bury logic that belongs in a named helper.

This Tessl package helps AI coding agents write, review, and refactor Java lambdas, method
references, functional interfaces, identity functions, no-op functional stages, suppliers,
predicates, consumers, and callbacks while preserving behavior.

The GitHub repository and Tessl plugin are private for now. Do not publish benchmark claims until
hosted evals are rerun and documented.

## Install

When the private package is available to your workspace:

| Tool | Command |
| --- | --- |
| npm | `npx tessl i martinfrancois/java-functional-style` |
| yarn | `yarn dlx tessl i martinfrancois/java-functional-style` |
| pnpm | `pnpx tessl i martinfrancois/java-functional-style` |
| bun | `bunx tessl i martinfrancois/java-functional-style` |
| Tessl CLI | `tessl i martinfrancois/java-functional-style` |

## What It Covers

- Java lambdas and method references
- `java.util.function` interfaces
- `Function.identity()` and `UnaryOperator.identity()`
- no-op identity stages such as `.map(x -> x)`
- callback readability and helper extraction
- supplier laziness
- side-effect boundaries in callbacks
- Java baseline compatibility for functional-style APIs

It is useful alone for general Java cleanup. It is also the recommended companion for:

- `martinfrancois/java-streams`
- `martinfrancois/java-optionals`

It does not force streams, Optionals, or functional style where a plain branch or loop is clearer.

## Ownership Boundaries

`java-functional-style` owns general Java lambda and functional-interface style.

`java-streams` owns stream and collector semantics.

`java-optionals` owns Optional semantics.

Install the domain skill and this package together when you want both semantic guidance and
callback-style guidance.

## Examples

Use an identity function when the API needs an identity mapper:

```java
Map<String, Card> cardsById = cards.stream()
        .collect(Collectors.toMap(
                Card::id,
                Function.identity(),
                CardIndex::preferActive,
                LinkedHashMap::new));
```

Remove a redundant identity stage instead of replacing it with another identity callback:

```java
String displayName = nameFromProfile.orElse(defaultName);
```

Extract callbacks that do real work:

```java
List<ShipmentNotice> notices = shipments.stream()
        .filter(shipment -> isOverdue(shipment, today))
        .map(shipment -> toNotice(shipment, today))
        .toList();
```

Keep expensive fallback work lazy:

```java
Profile profile = cachedProfile.orElseGet(() -> loadProfileFromRemote(userId));
```

## Contributing

The repository is open-source-ready while private: MIT licensed, with contribution, security, and
AI contribution policies. Real Tessl publish must not run until François explicitly asks.

Before any PR is opened, the composed setup must prove equal or better behavior than the current
domain-skill baselines on existing evals. Local validation alone is not enough for that gate.

## License

MIT
