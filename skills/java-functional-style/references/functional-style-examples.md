# Java Functional Style Examples

These examples are reusable runtime guidance, not scenario solutions. Apply them only when they
preserve the task's behavior, Java baseline, imports, null handling, ordering, laziness, side
effects, and object identity where observable.

## Identity Function Arguments

Use `Function.identity()` when the target API requires an identity `Function<T, T>`.

Before:

```java
Map<State, Integer> counts = states.stream()
        .collect(Collectors.toMap(
                state -> state,
                state -> 1,
                Integer::sum,
                HashMap::new));
```

After:

```java
import java.util.function.Function;

Map<State, Integer> counts = states.stream()
        .collect(Collectors.toMap(
                Function.identity(),
                state -> 1,
                Integer::sum,
                HashMap::new));
```

For identity value mappers, preserve the key mapper, merge function, and map supplier:

Before:

```java
Map<String, Card> cardsById = cards.stream()
        .collect(Collectors.toMap(
                Card::id,
                card -> card,
                CardIndex::preferActive,
                LinkedHashMap::new));
```

After:

```java
import java.util.function.Function;

Map<String, Card> cardsById = cards.stream()
        .collect(Collectors.toMap(
                Card::id,
                Function.identity(),
                CardIndex::preferActive,
                LinkedHashMap::new));
```

Do not replace a non-identity callback with `Function.identity()`:

```java
Collectors.toMap(Card::id, card -> card.normalized(), merge, LinkedHashMap::new)
```

The value mapper transforms the card, so it is not an identity function.

Use `UnaryOperator.identity()` only when the API specifically wants a `UnaryOperator<T>`:

```java
UnaryOperator<String> unchanged = UnaryOperator.identity();
```

## Remove No-Op Functional Stages

Before:

```java
String displayName = nameFromProfile
        .map(value -> value)
        .orElse(defaultName);
```

After:

```java
String displayName = nameFromProfile.orElse(defaultName);
```

Before:

```java
List<String> normalized = names.stream()
        .map(Function.identity())
        .map(String::trim)
        .toList();
```

After:

```java
List<String> normalized = names.stream()
        .map(String::trim)
        .toList();
```

Do not remove identity stages when the API boundary itself is observable:

```java
CompletableFuture<Order> sameOrder = future.thenApply(Function.identity());
```

This can be a deliberate completion-stage boundary. Remove it only when the surrounding behavior
proves the extra stage is unnecessary.

## Extract Block Callback Helpers

Keep callbacks as glue. Extract temporary values and branching into a helper.

Before:

```java
List<ShipmentNotice> notices = shipments.stream()
        .filter(shipment -> shipment.deliveredAt().isEmpty()
                && shipment.dueDate().isBefore(today))
        .map(shipment -> {
            long daysLate = ChronoUnit.DAYS.between(shipment.dueDate(), today);
            String severity = daysLate >= 14 ? "critical" : "late";
            return new ShipmentNotice(shipment.id(), shipment.customerEmail(), daysLate, severity);
        })
        .toList();
```

After:

```java
List<ShipmentNotice> notices = shipments.stream()
        .filter(shipment -> isOverdue(shipment, today))
        .map(shipment -> toNotice(shipment, today))
        .toList();

private static boolean isOverdue(Shipment shipment, LocalDate today) {
    return shipment.deliveredAt().isEmpty() && shipment.dueDate().isBefore(today);
}

private static ShipmentNotice toNotice(Shipment shipment, LocalDate today) {
    long daysLate = ChronoUnit.DAYS.between(shipment.dueDate(), today);
    return new ShipmentNotice(
            shipment.id(),
            shipment.customerEmail(),
            daysLate,
            daysLate >= 14 ? "critical" : "late");
}
```

## Name Multi-Condition Predicates

Before:

```java
List<Customer> billable = customers.stream()
        .filter(customer -> customer.active()
                && customer.paymentMethod() != null
                && !customer.suspended()
                && customer.balance().signum() > 0)
        .toList();
```

After:

```java
List<Customer> billable = customers.stream()
        .filter(BillingRules::isBillable)
        .toList();

private static boolean isBillable(Customer customer) {
    return customer.active()
            && customer.paymentMethod() != null
            && !customer.suspended()
            && customer.balance().signum() > 0;
}
```

## Keep Supplier Fallbacks Lazy

Before:

```java
Profile fallback = loadProfileFromRemote(userId);
Profile profile = cachedProfile.orElse(fallback);
```

After:

```java
Profile profile = cachedProfile.orElseGet(() -> loadProfileFromRemote(userId));
```

For cache misses, keep creation inside the mapping function:

```java
Widget widget = widgets.computeIfAbsent(id, WidgetFactory::create);
```

Do not precompute the widget before `computeIfAbsent` unless it is intentionally eager.

## Keep Checked Boundaries Clear

Do not hide checked IO or parsing contracts inside broad unchecked lambda wrappers when a plain
branch or named helper makes the behavior clearer.

Before:

```java
Optional<Config> config = path
        .map(p -> {
            try {
                return parseConfig(Files.readString(p));
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        });
```

After:

```java
Optional<Config> config = Optional.empty();
if (path.isPresent()) {
    config = Optional.of(parseConfig(Files.readString(path.get())));
}
```

Or use a named helper when the surrounding contract already accepts unchecked wrapping:

```java
Optional<Config> config = path.map(ConfigLoader::readUnchecked);
```

The helper name makes the exception boundary explicit.

## Side Effects

Avoid external mutation from callbacks when the API can produce the result directly.

Before:

```java
List<String> labels = new ArrayList<>();
items.stream()
        .map(Item::label)
        .forEach(label -> labels.add(label));
```

After:

```java
List<String> labels = items.stream()
        .map(Item::label)
        .toList();
```

Keep a callback side effect when the side effect is the requested outcome:

```java
events.forEach(auditLog::record);
```

If the callback may run in parallel or asynchronously, verify that the side effect is safe for that
execution mode.

## Do Not Force Functional Style

Use plain Java when it communicates the behavior better:

```java
List<String> readValidLines(Path path) throws IOException {
    List<String> result = new ArrayList<>();
    for (String line : Files.readAllLines(path)) {
        if (line.isBlank()) {
            continue;
        }
        if (line.startsWith("#")) {
            break;
        }
        result.add(line.trim());
    }
    return result;
}
```

A callback-heavy rewrite would obscure the checked IO and early-exit behavior. In a review, the
safe direction is to keep this loop or extract a small named helper, not to propose a clever
`dropWhile`/`takeWhile` stream chain by default.
