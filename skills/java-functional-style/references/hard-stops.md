# Java Functional Style Hard Stops

Use this before finalizing any change that touches lambdas, method references, functional
interfaces, callbacks, suppliers, identity functions, or no-op functional stages.

## Replacement antipatterns

Fix or explicitly classify each of these before finalizing:

- An identity lambda where the API requires `Function<T, T>` (`x -> x`, `item -> item`,
  `Function<T, T> f = value -> value`). Use `Function.identity()` and import
  `java.util.function.Function`.
- An identity lambda where the declared type is `UnaryOperator<T>`. Use
  `UnaryOperator.identity()` and import `java.util.function.UnaryOperator`.
- A hand-written identity helper (`private static <T> T same(T value)`) used only as a callback.
  Use the JDK helper the target API expects.
- A no-op stage: `.map(x -> x)`, `.map(Function.identity())`, `.filter(x -> true)`,
  `.peek(x -> {})`, or an `Optional.map` identity. Remove it when the stage is unobservable; do
  not "fix" it by swapping in another identity callback.
- A non-identity callback replaced by an identity helper. Copying, normalizing, validating,
  logging, unwrapping, casting, or calling another method is not identity.
- A block lambda (`item -> { ... }`) for ordinary value flow in `map`, `filter`, collector
  callbacks, Optional callbacks, `computeIfAbsent`, `merge`, completion stages, or listeners when
  a named helper or plain branch would be clearer.
- A callback whose arrow body starts on the next line or continues a nested fluent chain on later
  lines. Keep callbacks as same-line glue or extract a helper.
- A helper extraction that only relocated the block lambda. Re-scan helper bodies and extract
  again, or use plain code, until every callback is glue.
- A predicate with more than one meaningful condition and no name.
- A callback body with local temporaries, branching, formatting, merge or tie-break rules,
  severity selection, or record construction from derived values. Extract a helper.
- A method reference that changes behavior: a receiver expression evaluated once at creation
  (`lookup()::method`), a receiver that can be null at creation, a different overload than the
  lambda called, swapped `Comparator` or `BiFunction` argument order, or boxing where
  `comparingInt`/`comparingLong`/`comparingDouble` exists.
- `try`/`catch` buried in a lambda to wrap a checked exception when that hides an IO, parser, or
  prompt boundary or changes the method's contract. Use a named checked helper or a plain branch
  unless the surrounding API already owns unchecked wrapping.
- Eager fallback work before a supplier-taking API: computing a default before `orElseGet`,
  building a value before `computeIfAbsent`, calling `requireNonNullElse(v, expensive())`, or
  prompting and parsing before the absence check.
- External mutation from a callback when the API can produce the result directly.
- A missing import after introducing `Function.identity()` or `UnaryOperator.identity()`.
- Java baseline drift: `Predicate.not` below Java 11, `Optional.ifPresentOrElse` or
  `Optional.stream` below Java 9, `Stream.toList()` below Java 16.
- An identity stage removed from an API where the returned stage, scheduling, async boundary,
  callback invocation, tracing, metrics, or exception wrapping is observable. Be careful with
  `CompletableFuture.thenApply(Function.identity())`.

## Review notes

- Name the target functional-interface contract before recommending an identity helper.
- Preserve merge functions, map suppliers, comparators, ordering expectations, null behavior, and
  Java baseline compatibility when changing collector callbacks.
- For a simple minimum or maximum merge, `BinaryOperator.minBy(Comparator.comparing(...))` beats
  an inline ternary when the comparator and tie behavior match.
- Keep supplier work lazy even when the supplier body is a single method call, if that method has
  meaningful cost or side effects.
- For stateful windows, sentinel loops, early exits, checked IO, prompts, parser boundaries, or
  mutation-heavy accumulation, recommend keeping the loop or branch. In a rejection review, do not
  offer an alternative pipeline snippet even as a counterexample; it distracts from the safe
  direction and can introduce new defects.

## Functional-style scan

Run this over touched Java files, then inspect and classify hits. The scan is deliberately broad:
hits are review prompts, not mechanical edit instructions.

```bash
echo "java-functional-style hard-stop scan v2"
rg -nUP "->\\s*\\{|->\\s*$|\\.map\\(\\s*([A-Za-z_$][\\w$]*)\\s*->\\s*\\1\\s*\\)|\\.map\\(\\s*(?:Function|UnaryOperator)\\.identity\\(\\)\\s*\\)|(?:Function|UnaryOperator)\\s*<[^;=]+>\\s+[A-Za-z_$][\\w$]*\\s*=\\s*([A-Za-z_$][\\w$]*)\\s*->\\s*\\2\\s*;|Collectors\\.toMap\\([^;\\n]*\\b([A-Za-z_$][\\w$]*)\\s*->\\s*\\3\\b|computeIfAbsent\\([^;\\n]*->\\s*\\{|orElseGet\\([^;\\n]*->\\s*\\{|requireNonNullElse\\(|\\.orElse\\([^)]*\\(|catch\\s*\\([^)]*Exception[^)]*\\)\\s*\\{|\\.forEach\\([^;\\n]*(?:add|put|append|set)\\(|Comparator\\.comparing\\(|\\)::[A-Za-z_$]|Predicate\\.not\\(|ifPresentOrElse\\(|Optional\\.stream\\(|Stream\\.toList\\(" <touched Java files>
```

For each hit decide: required fix, acceptable domain-specific callback, Java baseline issue, or an
intentional side effect.
