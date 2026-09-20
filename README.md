# Java Functional Style Skill for AI Agents

Java callbacks are easy to make plausible and hard to keep honest. A hand-written `x -> x` hides
that an API wanted `Function.identity()`, a block lambda buries logic that belongs in a named
method, an eager `orElse(load())` defeats the laziness the API offers, and a method reference can
quietly change when its receiver is evaluated.

This Tessl package teaches AI coding agents to write, review, and refactor Java lambdas, method
references, and functional-interface callbacks (`Function`, `Predicate`, `Supplier`, `Consumer`,
`Comparator`, `BiFunction`) so they stay readable while preserving behavior.

The GitHub repository and the Tessl plugin are private for now.

## Contents

- [Getting Started](#getting-started)
- [Why This Exists](#why-this-exists)
- [What It Helps With](#what-it-helps-with)
- [Ownership Boundaries](#ownership-boundaries)
- [Examples](#examples)
- [How It's Evaluated](#how-its-evaluated)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

| Tool | Command |
| --- | --- |
| npm | `npx tessl i martinfrancois/java-functional-style` |
| yarn | `yarn dlx tessl i martinfrancois/java-functional-style` |
| pnpm | `pnpx tessl i martinfrancois/java-functional-style` |
| bun | `bunx tessl i martinfrancois/java-functional-style` |
| Tessl CLI | `tessl i martinfrancois/java-functional-style` |

The package ships one skill (`java-functional-style`) and one always-on rule with the same
conventions, so the guidance applies to any Java edit even when the agent does not activate the
skill on its own.

## Why This Exists

Two pieces of maintainer feedback started this package. A reviewer of the Java Streams skill
pointed out that agents keep writing multi-line lambdas instead of extracting a method
([lambdas are glue code](http://blog.agiledeveloper.com/2015/06/lambdas-are-glue-code.html)), and a
cleanup sweep produced `Collectors.toMap(state -> state, ...)` where `Function.identity()` was the
obvious choice. Both are general Java callback habits, not stream or Optional semantics, so they
belong in a package that any Java skill can sit next to.

## What It Helps With

- `Function.identity()` and `UnaryOperator.identity()` where an API needs an identity callback
- removing no-op stages such as `.map(x -> x)` instead of renaming them
- extracting named helpers and predicates from block or multi-condition callbacks
- keeping fallback work lazy in `orElseGet`, `computeIfAbsent`, and `requireNonNullElseGet`
- method references that keep receiver timing, overload choice, argument order, and boxing intact
- checked exceptions kept at a visible boundary instead of buried in a callback
- side-effecting callbacks only where the side effect is the point and safe for the execution mode
- Java baseline compatibility for functional APIs (`Predicate.not`, `ifPresentOrElse`, `toList()`)
- knowing when a plain loop or branch is the better shape, and saying so in reviews

It does not force streams, Optionals, or functional style where a loop or branch is clearer.

## Ownership Boundaries

`java-functional-style` owns general Java lambda and functional-interface style.

[`java-streams`](https://github.com/martinfrancois/java-streams-skill) owns stream and collector
semantics. [`java-optionals`](https://github.com/martinfrancois/java-optionals-skill) owns Optional
semantics.

Each package works on its own. Install the domain skill and this package together when you want
both semantic guidance and callback-style guidance.

## Examples

Use the JDK identity helper when the API needs one:

```java
Map<String, Exhibit> exhibitsById = exhibits.stream()
        .collect(Collectors.toMap(Exhibit::id, Function.identity(), Gallery::keepEarlier, LinkedHashMap::new));
```

Remove a redundant identity stage instead of replacing it with another one:

```java
String title = exhibitTitle.orElse(fallbackTitle);
```

Extract callbacks that do real work:

```java
List<MaintenanceAlert> alerts = readings.stream()
        .filter(reading -> exceedsHumidityLimit(reading, limits))
        .map(reading -> toAlert(reading, limits))
        .toList();
```

Keep expensive fallback work lazy:

```java
Settings settings = Objects.requireNonNullElseGet(loaded, this::buildDefaults);
```

## How It's Evaluated

The skill is tested on Java implementation, review, and cleanup tasks that involve callbacks. Each
task is run without the skill and with the skill, then scored on whether the agent keeps the
requested behavior while writing clearer callback code.

The evals cover the places where agents write plausible but weak callbacks: hand-written identity
lambdas, block lambdas with derived values and branching, eager fallback computation, method
references that change behavior, checked exceptions wrapped inside callbacks, and forced functional
rewrites of code that reads better as a loop.

Published scores will be shown on the Tessl plugin page once the package is public.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local validation, eval design rules, commit-message
format, and release workflow details.

AI-assisted contributions are welcome when they are transparent, reviewed, and owned by a human. See
[AI_CONTRIBUTION_POLICY.md](AI_CONTRIBUTION_POLICY.md).

For suspected vulnerabilities, use the private reporting path in [SECURITY.md](SECURITY.md).

## License

MIT
