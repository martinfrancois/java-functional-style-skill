# Review a method-reference cleanup

Use `$java-functional-style` to create `review.md`. Assume Java 17.

A teammate proposes this cleanup of `PairingBoard`. Review whether it should be accepted. Keep the
review concise and include a safer replacement snippet if you recommend changes.

Original:

```java
final class PairingBoard {
    private RatingSource source;
    private final Supplier<Ratings> ratings;

    PairingBoard(RatingSource initial) {
        this.source = initial;
        this.ratings = () -> source.snapshot();
    }

    void reload(RatingSource replacement) {
        this.source = replacement;
    }

    List<String> whitePlayers(List<Pairing> pairings) {
        return pairings.stream().map(p -> p.white()).toList();
    }

    int ratingOf(String player) {
        return ratings.get().of(player);
    }
}
```

Proposed:

```java
final class PairingBoard {
    private RatingSource source;
    private final Supplier<Ratings> ratings;

    PairingBoard(RatingSource initial) {
        this.source = initial;
        this.ratings = source::snapshot;
    }

    void reload(RatingSource replacement) {
        this.source = replacement;
    }

    List<String> whitePlayers(List<Pairing> pairings) {
        return pairings.stream().map(Pairing::white).toList();
    }

    int ratingOf(String player) {
        return ratings.get().of(player);
    }
}
```

`reload` is called between rounds so later ratings come from the replacement source.
