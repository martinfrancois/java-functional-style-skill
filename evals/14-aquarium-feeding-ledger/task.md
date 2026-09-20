# Aquarium feeding ledger

Use `$java-functional-style` to create `FeedingLedger.java`. Assume Java 17.

Implement a final class `FeedingLedger` with these methods and keep the nested records in the same
file:

```java
Map<String, FeedingTotal> totalsByTank(List<Feeding> feedings)
Map<String, List<Feeding>> feedingsByKeeper(List<Feeding> feedings)
CompletableFuture<TankReport> reportFor(String tankId, CompletableFuture<List<Feeding>> pending)
```

- `totalsByTank` accumulates one `FeedingTotal` per tank id: the total grams, the number of
  feedings, and the latest `fedAt` instant. Build it with `Map.merge` over the feedings and keep
  tank encounter order.
- `feedingsByKeeper` groups feedings by `keeper` in encounter order; use `computeIfAbsent` to
  create each keeper's list.
- `reportFor` transforms the pending feedings into a `TankReport` for the given tank: the tank id,
  the count of feedings whose `tankId` matches, and the sum of their grams. Use `thenApply` on the
  given future.

```java
record Feeding(String tankId, String keeper, int grams, Instant fedAt) {}
record FeedingTotal(int grams, int count, Instant latest) {}
record TankReport(String tankId, int feedings, int grams) {}
```

Do not add dependencies, caching, concurrency changes, or extra public API.
