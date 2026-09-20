# Podcast episode digests

Create `EpisodeDigests.java`. Assume Java 17.

Implement a final class `EpisodeDigests` with this method and keep the nested records in the same
file:

```java
List<EpisodeDigest> digests(List<Episode> episodes, Clock clock)
```

Include an episode when it is published, is not marked explicit, and is longer than 10 minutes.
For each included episode build an `EpisodeDigest` with the episode id, the title, the whole
number of days between `publishedAt` and today (from the clock), and the label `"fresh"` when
that is at most 7 days, otherwise `"archive"`. Keep encounter order.

```java
record Episode(String id, String title, LocalDate publishedAt, Duration length, boolean published, boolean explicit) {}
record EpisodeDigest(String id, String title, long ageDays, String label) {}
```

Do not add dependencies, caching, or extra public API.
