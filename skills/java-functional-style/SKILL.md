---
name: java-functional-style
license: MIT
description: Write, review, and refactor Java lambdas, method references, functional interfaces, callbacks, predicates, functions, suppliers, consumers, identity functions, no-op functional stages, and multi-line lambdas for behavior-preserving readability. Use for Function.identity(), UnaryOperator.identity(), identity lambdas, block lambdas, callback extraction, supplier laziness, and functional-style cleanup. Do not use to force functional style where plain Java is clearer.
---

# Java Functional Style

Preserve requested behavior, public API/artifact shape, ordering, laziness, exceptions, null
behavior, side effects, mutability, object identity where observable, and Java-version
compatibility. For implementation prompts, create the requested artifact before explaining. Do not
turn plain Java into callbacks, streams, or Optional chains when a branch or loop is clearer.

## Reference Bundle

| File | Purpose |
| --- | --- |
| [hard-stops.md](references/hard-stops.md) | Functional-style replacement antipatterns and the final scan |
| [functional-style-examples.md](references/functional-style-examples.md) | Before/after examples for identity functions, no-op stages, helper extraction, laziness, and side effects |
| [java-functional-api.md](references/java-functional-api.md) | Java baseline notes for functional interfaces and callback-related APIs |

## Core Workflow

When the prompt asks for a named artifact such as `review.md` or a Java source file, create that
exact file. Do not answer only in chat when a file artifact is requested.

1. Check the Java baseline first. Use [java-functional-api.md](references/java-functional-api.md)
   for minimum versions and fallbacks. Do not use APIs unavailable for the stated baseline.
2. Identify the functional-interface contract before changing code:
   `Function`, `UnaryOperator`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`,
   `BinaryOperator`, `Comparator`, or callbacks such as `map`, `flatMap`, `filter`,
   `orElseGet`, `ifPresent`, `computeIfAbsent`, `removeIf`, stream operations, collector
   callbacks, and completion callbacks.
3. Prefer a method reference only when it names the exact operation clearly and preserves behavior.
   Do not replace a lambda with a method reference if argument order, receiver binding, null
   behavior, checked exceptions, or overload resolution would change.
4. Use `Function.identity()` when an API needs an identity `Function<T, T>`. Use
   `UnaryOperator.identity()` when an API specifically needs an identity `UnaryOperator<T>`.
   Keep required imports. Do not replace non-identity callbacks such as `card -> card.copy()` or
   `value -> normalize(value)` with identity functions.
5. Remove no-op identity stages when the stage itself has no semantic purpose. A redundant
   `.map(x -> x)` is usually removed, not replaced with `.map(Function.identity())`. Do not remove
   a stage when scheduling, callback invocation, tracing, metrics, exception wrapping, or returned
   stage identity is observable.
6. Keep lambdas as glue. Use one-expression callbacks or method references for direct projection,
   filtering, consumption, or construction.
7. Extract a named helper, or use a plain branch, when a callback needs branching, local temporary
   variables, loops, checked work, nested fluent chains, merge rules, formatting, or more than one
   meaningful condition. This includes stream lambdas from the streams package: block lambdas,
   arrows whose body starts on the next line, and nested callback bodies that continue on later
   lines should become helpers when they do non-trivial work.
8. Keep supplier work lazy. Expensive fallback construction, IO, prompts, parsing, logging, or
   exception creation that is meant to happen only on absence/miss must stay inside the supplier
   passed to `orElseGet`, `computeIfAbsent`, or similar APIs.
9. Avoid external mutation from callbacks when the API can produce the result directly. Keep a
   callback side effect only when the side effect is the requested outcome and is safe for the
   chosen execution mode.
10. Keep plain branches or loops when they are clearer for checked IO, prompts, parser boundaries,
    complex early exits, sentinel-controlled windows, mutation-heavy logic, or behavior that depends
    on step-by-step control flow. In reviews of proposed functional rewrites for these shapes,
    reject behavior changes and say the loop or branch is the appropriate shape; do not offer a
    clever stream, Optional, or callback pipeline unless the user specifically asks for one and it
    is proven behavior-preserving.
11. Verify changed branches for present values, absent values, empty inputs, null behavior,
    ordering, side effects, laziness, exceptions, object identity where observable, and Java
    baseline compatibility.
12. Run the functional-style hard-stop scan from [hard-stops.md](references/hard-stops.md) and
    reconcile hits before finalizing.

## Quick Shapes

```java
cards.stream().collect(Collectors.toMap(Card::id, Function.identity(), merge, LinkedHashMap::new));
```

```java
return optional.orElse(defaultValue); // not optional.map(x -> x).orElse(defaultValue)
```

## Review Output

- Give a direct behavior-preserving decision plus one safe snippet when useful.
- Create `review.md` when requested, even for rejection-only reviews.
- For reviews rejecting a forced functional rewrite, do not include alternative stream, Optional, or
  callback-heavy snippets as examples or counterexamples. Recommend keeping the loop/branch or a
  small named helper.
- Explain code behavior, not internal workflow.
- Avoid internal workflow labels such as "per the skill", "hard stop", "marker", "scan",
  "checklist", "rubric", or "criteria" unless the user asks about the workflow itself.
