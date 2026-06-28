# Java functional style

When writing or reviewing Java code, keep lambdas and functional-interface callbacks as intent-revealing glue.

Prefer method references or named JDK functions when they express the exact operation clearly. When an API requires an identity `Function<T, T>`, use `Function.identity()` instead of a hand-written identity lambda such as `x -> x`. When an API specifically requires an identity `UnaryOperator<T>`, use `UnaryOperator.identity()`.

Do not add no-op functional stages. Remove identity mapping stages such as `stream.map(x -> x)`, `stream.map(Function.identity())`, `optional.map(x -> x)`, or `optional.map(Function.identity())` when removing the stage preserves behavior.

Extract a named helper, or use a plain branch, when a lambda or callback needs branching, local temporary variables, loops, checked exception handling, nested fluent chains, side effects, or more than one meaningful condition.

Preserve ordering, laziness, exception behavior, side effects, mutability, object identity where observable, and Java baseline compatibility. Do not replace a non-identity lambda with an identity function merely because the lambda is short.
