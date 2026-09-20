# Java functional style

When writing or reviewing Java, keep lambdas and functional-interface callbacks as one-expression
glue that names a single step of the value flow.

- Use `Function.identity()` when an API needs an identity `Function<T, T>` and
  `UnaryOperator.identity()` when the declared type is `UnaryOperator<T>`, instead of `x -> x`.
- Remove no-op stages such as `.map(x -> x)` or `.map(Function.identity())` when removing them
  preserves behavior; do not replace one identity callback with another.
- Extract a named helper, or use a plain branch, when a callback needs branching, local
  temporaries, loops, checked exception handling, a merge or tie-break rule, formatting, more than
  one meaningful condition, or a nested fluent chain. Re-scan the helper afterwards; relocating a
  block lambda is not extraction.
- Keep fallback work lazy: inside `orElseGet`, `computeIfAbsent`, `requireNonNullElseGet`, or the
  supplier the API takes, never computed before the absence check.
- Prefer a method reference only when it keeps receiver timing, overload choice, argument order,
  boxing, and exception behavior unchanged.
- Keep plain loops and branches for checked IO, prompts, parser boundaries, early exits,
  sentinel-driven windows, and mutation-heavy accumulation. Do not force streams, Optionals, or
  callback chains where a branch or loop is clearer, and in a review of such a rewrite recommend
  keeping the loop rather than proposing a cleverer pipeline.
- Preserve ordering, laziness, exception behavior, side effects, mutability, observable object
  identity, and the project's Java baseline in every change.
- In user-facing output such as `review.md`, explain the Java behavior only; do not mention rules,
  skills, rubrics, criteria, or internal file names unless the user asks about the workflow.
