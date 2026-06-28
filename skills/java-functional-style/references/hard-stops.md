# Java Functional Style Hard Stops

Use this reference before finalizing Java functional-style cleanup or first-pass implementation
when the code touches lambdas, method references, functional interfaces, callbacks, suppliers,
identity functions, or no-op functional stages.

## Replacement Antipatterns

Fix or explicitly classify these before finalizing:

- Identity lambdas where an API requires `Function<T, T>`, such as `x -> x`, `value -> value`,
  `card -> card`, or `Function<T, T> f = item -> item`. Use `Function.identity()` and import
  `java.util.function.Function`.
- Identity lambdas where an API specifically requires `UnaryOperator<T>`, such as
  `UnaryOperator<String> op = value -> value`. Use `UnaryOperator.identity()` and import
  `java.util.function.UnaryOperator`.
- Custom identity helpers such as `private static <T> T identity(T value) { return value; }` used
  only as a functional callback. Prefer the JDK identity function required by the target API.
- No-op functional stages such as `.map(x -> x)`, `.map(value -> value)`,
  `.map(Function.identity())`, or `.map(UnaryOperator.identity())` when removing the stage preserves
  behavior. Do not "fix" a redundant map by replacing it with another identity map.
- Replacement of non-identity lambdas with identity functions. A callback that copies, normalizes,
  validates, logs, unwraps, casts, transforms, or calls another method is not an identity callback.
- Block lambdas for ordinary value flow: `item -> { ... }` inside `map`, `filter`, collector
  callbacks, Optional callbacks, `computeIfAbsent`, completion stages, or similar APIs when a named
  helper or plain branch would be clearer.
- Arrows whose body starts on the next line, or callback bodies that continue nested fluent chains
  on later lines. Keep callbacks as same-line glue or extract helpers.
- Predicate callbacks with more than one meaningful condition when a named predicate would explain
  the rule better.
- Callback bodies with local temporary variables, branching, formatting, merge rules, severity
  selection, record construction with derived values, or nested fluent chains. Extract a helper.
- Checked exception handling buried in lambdas when it changes the contract or hides IO, parser, or
  prompt boundaries. Use a named checked helper or a plain branch unless the surrounding API
  explicitly owns unchecked wrapping.
- Eager fallback work before supplier-taking APIs, such as computing an expensive default before
  `orElseGet`, constructing a cache value before `computeIfAbsent`, or prompting/parsing before an
  absence check.
- External mutation from callbacks when the API can produce the result directly. A callback side
  effect may remain only when the side effect is the operation's purpose and is safe.
- Missing imports caused by using `Function.identity()` or `UnaryOperator.identity()`.
- Java baseline drift: `Predicate.not`, `Optional.ifPresentOrElse`, `Optional.stream`, or
  `Stream.toList()` used below their minimum Java version.
- Removing identity callback stages from APIs where the returned stage object, scheduling, async
  boundary, callback invocation, tracing, metrics, exception wrapping, or object identity is
  observable. Be careful with `CompletableFuture.thenApply(Function.identity())`.

## Review Notes

- Name the target functional-interface contract before recommending an identity helper.
- Preserve merge functions, map suppliers, comparators, ordering expectations, null behavior, and
  Java baseline compatibility when changing collector callbacks.
- Keep supplier work lazy even when the supplier body is only one method call if that method has
  meaningful cost or side effects.
- Keep plain branches or loops for complex early exits, mutation-heavy output, checked IO, prompts,
  parser boundaries, or stateful algorithms.

## Functional-Style Scan

Run this scan over touched Java files, then inspect and classify hits. The scan is broad by design:
hits are review prompts, not mechanical edit instructions.

```bash
echo "java-functional-style hard-stop scan v1"
rg -nUP "->\\s*\\{|->\\s*$|\\.map\\(\\s*(?:[A-Za-z_$][\\w$]*)\\s*->\\s*\\1\\s*\\)|\\.map\\(\\s*(?:Function|UnaryOperator)\\.identity\\(\\)\\s*\\)|(?:Function|UnaryOperator)\\s*<[^;=]+>\\s+[A-Za-z_$][\\w$]*\\s*=\\s*([A-Za-z_$][\\w$]*)\\s*->\\s*\\1\\s*;|Collectors\\.toMap\\([^;\\n]*(\\b[A-Za-z_$][\\w$]*\\b)\\s*->\\s*\\1|computeIfAbsent\\([^;\\n]*->\\s*\\{|orElseGet\\([^;\\n]*->\\s*\\{|catch\\s*\\([^)]*Exception[^)]*\\)\\s*\\{|\\.forEach\\([^;\\n]*(?:add|put|append|set)\\(|Predicate\\.not\\(|ifPresentOrElse\\(|Optional\\.stream\\(|Stream\\.toList\\(" <touched Java files>
```

For each hit, decide whether it is a required fix, an acceptable domain-specific callback, a Java
baseline issue, or an intentionally side-effecting operation.
