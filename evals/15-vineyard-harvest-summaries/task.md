# Vineyard harvest summaries

Create `HarvestSummaries.java`. Assume Java 17.

Implement a final class `HarvestSummaries` with these methods and keep the nested records in the
same file:

```java
Optional<HarvestNote> noteFor(Optional<Plot> plot, LocalDate today)
Map<String, VarietyStats> statsByVariety(List<Harvest> harvests)
List<String> crateLabels(List<Harvest> harvests)
```

- `noteFor` maps a present plot to a `HarvestNote` with the plot id, the whole number of days
  since `plantedAt` up to today, and the readiness `"ready"` when that is at least 1095 days,
  otherwise `"young"`. An absent plot gives an empty result. Use `Optional.map`.
- `statsByVariety` groups harvests by `variety` and reduces each group to a `VarietyStats` with
  the number of crates, the total kilograms, and the average kilograms per crate rounded to one
  decimal (`Math.round(x * 10) / 10.0`). Use `Collectors.groupingBy` with a downstream collector.
- `crateLabels` produces one label per harvest in encounter order, formatted as
  `<variety>-<plotId>-<kilograms>kg`, with the variety upper-cased and the kilograms without
  decimals (`%.0f`). Use a stream pipeline over the harvests.

```java
record Plot(String id, LocalDate plantedAt) {}
record Harvest(String plotId, String variety, double kilograms) {}
record HarvestNote(String plotId, long daysSincePlanting, String readiness) {}
record VarietyStats(int crates, double totalKilograms, double averageKilograms) {}
```

Do not add dependencies, caching, or extra public API.
