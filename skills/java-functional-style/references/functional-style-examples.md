# Java Functional Style Examples

Reusable shapes, not answers to any particular task. Apply one only when it keeps the task's
behavior, Java baseline, imports, null handling, ordering, laziness, side effects, and observable
object identity.

## Identity function arguments

When the API wants an identity `Function<T, T>`, say so with the JDK helper:

```java
import java.util.function.Function;

Map<String, Exhibit> exhibitsById = exhibits.stream()
        .collect(Collectors.toMap(Exhibit::id, Function.identity(), Gallery::keepEarlier, LinkedHashMap::new));
```

Keep the key mapper, merge function, and map supplier exactly as they were. A registry of named
transforms uses the same helper for its "unchanged" entry:

```java
Map<String, UnaryOperator<String>> captionStyles = Map.of(
        "plain", UnaryOperator.identity(),
        "upper", String::toUpperCase,
        "trimmed", String::strip);
```

Do not turn a real transformation into an identity helper:

```java
Collectors.toMap(Exhibit::id, Exhibit::summary, Gallery::keepEarlier, LinkedHashMap::new) // summary() maps, keep it
```

## Remove no-op stages

```java
// before
String title = exhibitTitle.map(value -> value).orElse(fallbackTitle);
// after
String title = exhibitTitle.orElse(fallbackTitle);
```

```java
// before
List<String> tagNames = rawTags.stream().map(Function.identity()).map(String::strip).toList();
// after
List<String> tagNames = rawTags.stream().map(String::strip).toList();
```

Keep an identity stage when the stage object itself is the point, for example a
`CompletableFuture.thenApply(Function.identity())` used as a deliberate completion boundary.
Remove it only when the surrounding code shows the extra stage is unobservable.

## Extract helpers from block callbacks

```java
// before
List<MaintenanceAlert> alerts = readings.stream()
        .filter(reading -> reading.sensor().active()
                && reading.humidity() > limits.maxHumidity()
                && !reading.sensor().muted())
        .map(reading -> {
            double excess = reading.humidity() - limits.maxHumidity();
            String level = excess > 15 ? "critical" : "warning";
            return new MaintenanceAlert(reading.sensor().id(), level, excess);
        })
        .toList();

// after
List<MaintenanceAlert> alerts = readings.stream()
        .filter(reading -> exceedsHumidityLimit(reading, limits))
        .map(reading -> toAlert(reading, limits))
        .toList();

private static boolean exceedsHumidityLimit(Reading reading, Limits limits) {
    return reading.sensor().active()
            && reading.humidity() > limits.maxHumidity()
            && !reading.sensor().muted();
}

private static MaintenanceAlert toAlert(Reading reading, Limits limits) {
    double excess = reading.humidity() - limits.maxHumidity();
    return new MaintenanceAlert(reading.sensor().id(), excess > 15 ? "critical" : "warning", excess);
}
```

Both callbacks were extracted: the multi-condition predicate got a name, and the block mapping
became a method whose body is plain code. Re-scan the helpers; they must not hide another block
lambda.

## Method references that change behavior

```java
Supplier<Tuner> tuner = registry.current()::tuner;      // registry.current() runs once, now
Supplier<Tuner> tuner = () -> registry.current().tuner(); // runs on every get()
```

Pick the one whose timing the code needs. The same applies to `this::field`-style references on
objects that may be null at creation time, and to overloaded methods where the reference resolves
to a different overload than the lambda did.

```java
// before: boxes every comparison
rehearsals.sort(Comparator.comparing(Rehearsal::durationMinutes));
// after
rehearsals.sort(Comparator.comparingInt(Rehearsal::durationMinutes));
```

## Keep supplier fallbacks lazy

```java
// before: the recipe is parsed even when the cache already has it
Recipe parsed = parseRecipe(source);
Recipe recipe = recipeCache.computeIfAbsent(source.id(), ignored -> parsed);
// after
Recipe recipe = recipeCache.computeIfAbsent(source.id(), ignored -> parseRecipe(source));
```

```java
// before: buildDefaults() always runs
Settings settings = Objects.requireNonNullElse(loaded, buildDefaults());
// after
Settings settings = Objects.requireNonNullElseGet(loaded, this::buildDefaults);
```

The same rule applies to `Optional.orElseGet`, `orElseThrow(() -> ...)`, and logging APIs that
accept a `Supplier`.

## Keep checked boundaries visible

```java
// before: the IOException contract is hidden inside the callback
List<Score> scores = files.stream()
        .map(file -> {
            try {
                return parseScore(Files.readString(file));
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        })
        .toList();

// after: the method that reads declares what it throws
List<Score> readScores(List<Path> files) throws IOException {
    List<Score> scores = new ArrayList<>();
    for (Path file : files) {
        scores.add(parseScore(Files.readString(file)));
    }
    return scores;
}
```

When the surrounding API already accepts unchecked wrapping, a named helper such as
`ScoreFiles::readUnchecked` makes the conversion visible instead of burying it in a block lambda.

## Side effects

```java
// before
List<String> badges = new ArrayList<>();
members.stream().map(Member::badgeName).forEach(badges::add);
// after
List<String> badges = members.stream().map(Member::badgeName).toList();
```

A side effect that is the requested outcome stays a callback (`events.forEach(auditLog::record)`),
but check that it is safe for parallel or asynchronous execution before keeping it.

## Plain Java when it reads better

```java
List<String> activeStanzas(List<String> lines) {
    List<String> result = new ArrayList<>();
    boolean inside = false;
    for (String line : lines) {
        if (line.equals("BEGIN")) {
            inside = true;
            continue;
        }
        if (line.equals("END")) {
            break;
        }
        if (inside && !line.isBlank()) {
            result.add(line.strip());
        }
    }
    return result;
}
```

A sentinel-driven window with an early exit reads best as this loop. In a review of a proposed
stream rewrite, say that the loop (or a named helper around it) is the right shape and reject the
behavior change; do not offer a cleverer pipeline as the "fixed" version.
