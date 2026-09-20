# Refactor callback mappers

Create `IdentityMapperCleanup.java`. Assume Java 17.

Clean up the callback style in this class without changing behavior:

```java
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

final class IdentityMapperCleanup {
    Map<String, Card> cardsById(List<Card> cards) {
        return cards.stream()
                .collect(Collectors.toMap(
                        Card::id,
                        card -> card,
                        IdentityMapperCleanup::preferActive,
                        LinkedHashMap::new));
    }

    Map<State, Integer> stateCounts(List<State> states) {
        return states.stream()
                .collect(Collectors.toMap(
                        state -> state,
                        state -> 1,
                        Integer::sum,
                        HashMap::new));
    }

    Map<String, CardSnapshot> snapshotsById(List<Card> cards) {
        return cards.stream()
                .collect(Collectors.toMap(
                        Card::id,
                        card -> card.snapshot(),
                        IdentityMapperCleanup::preferNewer,
                        LinkedHashMap::new));
    }

    private static Card preferActive(Card left, Card right) {
        return right.active() && !left.active() ? right : left;
    }

    private static CardSnapshot preferNewer(CardSnapshot left, CardSnapshot right) {
        return right.version() > left.version() ? right : left;
    }

    record Card(String id, boolean active, int version) {
        CardSnapshot snapshot() {
            return new CardSnapshot(id, version);
        }
    }

    record CardSnapshot(String id, int version) {}
    record State(String code) {}
}
```

Keep all three methods and the nested records in the same file. Do not change the merge rules,
returned map type, key selection, or snapshot conversion.
