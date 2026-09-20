# Bike station fallbacks

Use `$java-functional-style` to create `StationResolver.java`. Assume Java 17.

Implement a final class `StationResolver` with these methods and keep the nested types in the
same file:

```java
Station resolve(String stationId, Map<String, Station> cache, StationDirectory directory)
Pricing pricingFor(Station station, Pricing configured)
```

- `resolve` returns the cached station when present. On a miss it fetches the station with
  `directory.fetch(stationId)`, stores it in the cache, and returns it. The directory call is slow
  and counts against a rate limit, so it must run only on a miss.
- `pricingFor` returns `configured` when it is non-null, otherwise `Pricing.standardFor(station)`.
  `standardFor` builds a full tariff table and is expensive; it must run only when `configured` is
  null.

```java
record Station(String id, String name) {}
record Pricing(String tariff) {
    static Pricing standardFor(Station station) { return new Pricing("standard-" + station.id()); }
}
interface StationDirectory { Station fetch(String stationId); }
```

Do not add dependencies, extra public API, or a different cache type.
