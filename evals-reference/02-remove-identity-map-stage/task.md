# Clean up identity stages

Create `IdentityStageCleanup.java`. Assume Java 17.

Clean up the redundant functional stages without changing behavior:

```java
import java.util.List;
import java.util.Optional;
import java.util.function.Function;

final class IdentityStageCleanup {
    String displayName(Optional<String> profileName, String defaultName) {
        return profileName
                .map(name -> name)
                .orElse(defaultName);
    }

    List<String> labels(List<String> input) {
        return input.stream()
                .map(Function.identity())
                .map(String::trim)
                .filter(label -> !label.isEmpty())
                .toList();
    }

    Optional<Integer> parsed(Optional<String> value) {
        return value
                .map(text -> text)
                .map(Integer::parseInt);
    }
}
```

Keep the same public behavior for present, absent, empty, and invalid values. Do not add external
dependencies or change method signatures.
