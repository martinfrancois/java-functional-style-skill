# Track name normalizers

Create `TrackNameNormalizers.java`. Assume Java 17.

A radio playlist tool applies a named normalizer to each track name before display. Implement a
final class `TrackNameNormalizers` with:

```java
Map<String, UnaryOperator<String>> normalizers()
String normalize(String mode, String trackName)
```

Modes:

- `"as-is"`: the name is returned unchanged.
- `"uppercase"`: the name in upper case.
- `"collapsed"`: leading and trailing whitespace removed and internal runs of whitespace collapsed
  to one space.

`normalize` looks the mode up in `normalizers()` and throws `IllegalArgumentException` naming the
unknown mode. The map must be unmodifiable and must not depend on insertion order. Do not add
dependencies or extra public API.
