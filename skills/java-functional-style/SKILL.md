---
name: java-functional-style
license: MIT
description: Write, review, and refactor Java lambdas, method references, and functional-interface callbacks (Function, Predicate, Supplier, Consumer, Comparator, BiFunction) so they stay readable and behavior-preserving. Use whenever Java code creates or changes a callback passed to a stream, Optional, Map, CompletableFuture, or listener API; when a cleanup or review touches identity lambdas (x returning x), block or multi-line lambdas, method references, suppliers, or side-effecting callbacks; or when the user asks to make Java code cleaner or more functional, even if they never say "lambda". Do not use for stream or Optional semantics themselves, and do not use it to force functional style where a plain loop or branch is clearer.
---

# Java Functional Style

Lambdas are glue. A callback should name one step of the value flow; everything else belongs in a
named method, a plain branch, or the JDK helper that already exists for it. Preserve requested
behavior, public API and artifact shape, ordering, laziness, exceptions, null behavior, side
effects, and Java-version compatibility while making callbacks readable.

For implementation prompts, create the requested artifact (a Java source file, `review.md`, or
whatever the prompt names) before explaining. When another Java domain skill is active, let it own
stream, collector, or Optional semantics; this skill only changes how callbacks are written.

## Reference Bundle

| File | Load it when |
| --- | --- |
| [hard-stops.md](references/hard-stops.md) | Before finalizing: the replacement antipatterns and the scan command |
| [functional-style-examples.md](references/functional-style-examples.md) | You want a before/after shape for identity functions, no-op stages, helper extraction, laziness, side effects, or plain Java |
| [java-functional-api.md](references/java-functional-api.md) | The project baseline is below Java 17, or you are unsure which functional API a baseline has |

## Workflow

1. Check the Java baseline first (build files, toolchains, CI, docs). If it is unclear, write Java
   8-compatible callbacks or state the assumption. See
   [java-functional-api.md](references/java-functional-api.md).
2. Name the functional-interface contract before touching a callback: `Function`,
   `UnaryOperator`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`, `BinaryOperator`,
   `Comparator`, or the callback parameter of `map`, `filter`, `orElseGet`, `computeIfAbsent`,
   `merge`, `removeIf`, `replaceAll`, `thenApply`, or a listener. The contract decides which JDK
   helper applies and which behaviors are observable.
3. Use the JDK identity helper when the API needs an identity callback. `Function.identity()`
   for a `Function<T, T>` (for example the value mapper of `Collectors.toMap`, a `groupingBy`
   downstream `mapping`, or a `Map<String, Function<...>>` "no transform" entry) and
   `UnaryOperator.identity()` when the declared type is `UnaryOperator<T>`. Write `x -> x` only
   where no functional interface is involved. Add the import. Never turn a callback that copies,
   normalizes, unwraps, casts, or calls something into an identity helper.

   ```java
   // before
   Map<String, Exhibit> byId = exhibits.stream().collect(Collectors.toMap(Exhibit::id, e -> e));
   // after
   Map<String, Exhibit> byId = exhibits.stream().collect(Collectors.toMap(Exhibit::id, Function.identity()));
   ```
4. Remove no-op stages instead of renaming them. `.map(x -> x)`, `.map(Function.identity())`,
   `.filter(x -> true)`, and `.peek(x -> {})` add nothing when the stage itself is unobservable.
   Keep a stage when the returned object, scheduling, callback invocation, tracing, or exception
   wrapping is observable (`CompletableFuture.thenApply(Function.identity())` can be a deliberate
   boundary).

   ```java
   // before
   String title = exhibitTitle.map(value -> value).orElse(fallbackTitle);
   // after
   String title = exhibitTitle.orElse(fallbackTitle);
   ```
5. Prefer a method reference only when it names the exact operation and keeps behavior. Check
   receiver binding (`expr::method` evaluates `expr` once, at creation, and throws `NullPointerException`
   there if it is null), overload resolution, argument order for `Comparator` and `BiFunction`,
   boxing (`Comparator.comparingInt` over `comparing` for primitives), and checked exceptions.
   When any of these change, keep the lambda or extract a helper.
6. Keep lambdas as one-expression glue. When a callback needs branching, local temporaries,
   loops, formatting, a merge or tie-break rule, more than one meaningful condition, or a nested
   fluent chain, extract a named helper (`toSummary(item, today)`, `isEligible(item)`) and pass
   `this::isEligible` or a one-line lambda. Name multi-condition predicates. Re-scan every
   extracted helper: moving a block lambda into a helper that still contains a block lambda is not
   done.
7. Keep supplier work lazy. Fallback construction, IO, prompts, parsing, and exception creation
   that should happen only on absence or miss belong inside the supplier passed to `orElseGet`,
   `orElseThrow`, `computeIfAbsent`, `Objects.requireNonNullElseGet`, or a logging supplier.
   `orElse(compute())` and `requireNonNullElse(value, compute())` always evaluate `compute()`.
8. Let the API produce the result. Do not mutate an external list, map, counter, or builder from
   a callback when the API can return the value (`toList`, `toMap`, `merge`, `reduce`). Keep a
   side-effecting callback only when the side effect is the requested outcome, and check it is
   safe for the execution mode (parallel, async, or listener threads).
9. Keep checked exceptions at a visible boundary. Do not bury `try`/`catch` inside a callback to
   wrap an `IOException` unless the surrounding API already owns unchecked wrapping. Use a named
   helper that declares or converts the exception on purpose, or a plain loop or branch.
10. Choose plain Java when it reads better: checked IO, prompts, parser boundaries, early exits,
    sentinel-driven windows, mutation-heavy accumulation, and step-by-step control flow. When
    reviewing a functional rewrite of such code, reject the behavior change and recommend keeping
    the loop or branch; do not counter-propose another pipeline.
11. Verify each changed callback for present and absent values, empty input, nulls, ordering,
    laziness, exception type and timing, side effects, object identity where observable, and the
    Java baseline. Then run the `rg` scan from [hard-stops.md](references/hard-stops.md) over
    the touched files and reconcile every hit before finishing.

## Gotchas

- `Optional.orElse(expensive())` and `Objects.requireNonNullElse(v, expensive())` evaluate the
  argument every time, even when the value is present.
- `Map.computeIfAbsent` must not modify the same map inside its mapping function; that throws
  `ConcurrentModificationException` on `HashMap` since Java 9.
- `service::handle` captures `service` when the reference is created; a lambda
  `x -> service.handle(x)` reads the field on every call. They differ when the field is reassigned
  or null at creation time.
- `Comparator.comparing(Item::price)` boxes primitives on every comparison; use `comparingInt`,
  `comparingLong`, or `comparingDouble`.
- `Predicate.not` needs Java 11, `Optional.ifPresentOrElse` and `Optional.stream` need Java 9,
  `Stream.toList()` needs Java 16.
- A lambda that captures a loop variable or a mutable local only compiles when the variable is
  effectively final; copy it into a final local rather than switching to an array or holder hack.

## Review Output

- Lead with the behavior-preserving decision, then at most one safe snippet.
- Create `review.md` when the prompt asks for it, even for a rejection-only review.
- Explain Java behavior. Do not mention skills, rules, rubrics, criteria, scans, checklists, or
  internal file names unless the user asks about the workflow itself.
