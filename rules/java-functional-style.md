# Java functional style

When writing or reviewing Java code, keep lambdas and functional-interface callbacks as intent-revealing glue.

Prefer method references or named JDK functions when they express the exact operation clearly. When an API requires an identity `Function<T, T>`, use `Function.identity()` instead of a hand-written identity lambda such as `x -> x`. When an API specifically requires an identity `UnaryOperator<T>`, use `UnaryOperator.identity()`.

Do not add no-op functional stages. Remove identity mapping stages such as `stream.map(x -> x)`, `stream.map(Function.identity())`, `optional.map(x -> x)`, or `optional.map(Function.identity())` when removing the stage preserves behavior.

Extract a named helper, or use a plain branch, when a lambda or callback needs branching, local temporary variables, loops, checked exception handling, nested fluent chains, side effects, collector merge tie-breaking, or more than one meaningful condition. Do not leave chained ternary merge callbacks inline. For nested stream callbacks, prefer `.flatMap(Type::childEntries)` over `.flatMap(parent -> parent.children().stream().filter(...).map(...))`. After extracting a helper, re-scan that helper too; do not just move a multi-line callback or nested fluent callback chain into the helper.

When reviewing a proposed functional rewrite of stateful windowing, sentinel-controlled loops, early breaks, or mutation-heavy accumulation, reject behavior changes and prefer keeping the clear loop or branch. Do not replace it with a clever stream, Optional, or callback pipeline merely because one can be written.

For those rejection reviews, do not stop at "reject": explicitly say to keep the original loop or a branch-based helper because that shape preserves the state, ordering, and early break. Do not mention a hypothetical `dropWhile`/`takeWhile` or other stream solution.

Preserve ordering, laziness, exception behavior, side effects, mutability, object identity where observable, and Java baseline compatibility. Do not replace a non-identity lambda with an identity function merely because the lambda is short.

In user-facing files such as `review.md`, explain the Java behavior only. Do not add rule, rules, or rule-compliance sections; do not quote internal guidance or mention skills, rubrics, criteria, internal paths, or this rule unless the user explicitly asks about the workflow.
