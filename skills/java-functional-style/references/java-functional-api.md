# Java Functional API Compatibility

Always infer the project Java baseline before choosing APIs. Check `pom.xml`, Maven compiler
settings, Gradle toolchains, `sourceCompatibility`, `targetCompatibility`, CI workflows,
`Dockerfile`, `.sdkmanrc`, `.java-version`, and project docs.

If the baseline is unclear, prefer Java 8-compatible code or state the assumption explicitly.

## Java 8 Functional Interfaces And Callbacks

| API or feature | Minimum Java | Notes |
| --- | ---: | --- |
| Lambdas | 8 | Keep callbacks as short behavior glue. |
| Method references | 8 | Use only when receiver binding, argument order, overload resolution, and null behavior stay clear. |
| `java.util.function.Function` | 8 | Use for `T -> R` callbacks. Use `Function.identity()` for required identity `Function<T, T>`. |
| `java.util.function.UnaryOperator` | 8 | Use for `T -> T` operators. Use `UnaryOperator.identity()` when the API specifically needs an identity unary operator. |
| `Predicate` | 8 | Use for boolean tests; extract named predicates when more than one meaningful condition hurts readability. |
| `Supplier` | 8 | Use to keep fallback work lazy. Do not compute expensive values before passing the supplier. |
| `Consumer` | 8 | Use for side effects only when the side effect is the requested outcome and safe. |
| `BiFunction` / `BinaryOperator` | 8 | Use for merge and combination callbacks; extract helpers for tie-breaking, nulls, or branching. |
| `Comparator` | 8 | Prefer comparing helpers when a comparison needs normalization, null handling, or multiple branches. |
| `Optional` callbacks | 8 | `map`, `flatMap`, `filter`, `orElseGet`, and `ifPresent` take callbacks; which Optional operation to use is the `java-optionals` skill's job. |
| Stream callbacks | 8 | `map`, `flatMap`, `filter`, and collector callbacks take callbacks; which stream operation or collector to use is the `java-streams` skill's job. |
| `Map.computeIfAbsent` | 8 | Mapping function is lazy per miss; keep expensive creation inside it and avoid externally precomputing the value. |
| `Collection.removeIf` / `List.replaceAll` | 8 | The callback mutates the collection by design; preserve that side effect deliberately. `replaceAll` takes a `UnaryOperator`. |
| `Map.merge` / `Map.compute` | 8 | Remapping callbacks; extract a helper when the merge rule branches. |
| `Objects.requireNonNullElseGet` | 9 | Lazy default for nullable values; `requireNonNullElse` evaluates its default eagerly. |

## Later Java Baselines

| API or feature | Minimum Java | Notes |
| --- | ---: | --- |
| `Optional.stream` | 9 | Optional flattening helper; Java 8 needs `filter(Optional::isPresent).map(Optional::get)`. |
| `Optional.ifPresentOrElse` | 9 | Use when both present and absent branches are clear callbacks. Use plain branches when checked work or complex flow is clearer. |
| `Predicate.not` | 11 | Readable for simple negated method references, such as `Predicate.not(String::isBlank)`. Do not obscure complex predicates. |
| `Optional.isEmpty` | 11 | Readability helper for absence checks. |
| `Stream.toList()` | 16 | Baseline note only: returns an unmodifiable list. Stream result semantics belong to `java-streams`. |
| Records | 16 | Useful for tiny carriers when a callback must preserve object plus derived value. |

## Imports

Using `Function.identity()` usually requires:

```java
import java.util.function.Function;
```

Using `UnaryOperator.identity()` usually requires:

```java
import java.util.function.UnaryOperator;
```

Prefer explicit imports that match the project style. Avoid adding wildcard imports unless the
surrounding file already uses them.

## Baseline Fallbacks

- Java 8 has all core functional interfaces needed for this skill.
- If `Predicate.not` is unavailable, keep a short negated lambda or extract a positively named
  helper.
- If `ifPresentOrElse` is unavailable, use a plain `if (optional.isPresent())` branch when both
  sides are meaningful.
- If a method reference becomes ambiguous on the project baseline or compiler settings, keep the
  lambda or extract a named helper with an explicit type.
