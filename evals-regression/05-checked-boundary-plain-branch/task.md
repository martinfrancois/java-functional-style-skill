# Clean up checked parsing boundary

Create `ConfigLoader.java`. Assume Java 17.

Clean up this class for readability without changing its checked exception contract:

```java
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;

final class ConfigLoader {
    Optional<Config> load(Optional<Path> configPath) throws IOException {
        return configPath.map(path -> {
            try {
                String raw = Files.readString(path);
                return parse(raw);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        });
    }

    private static Config parse(String raw) {
        String trimmed = raw.trim();
        if (trimmed.isEmpty()) {
            throw new IllegalArgumentException("empty config");
        }
        return new Config(trimmed);
    }

    record Config(String body) {}
}
```

The method should still throw `IOException` from file reading, still throw
`IllegalArgumentException` for empty config content, and still return `Optional.empty()` when no path
is provided.
