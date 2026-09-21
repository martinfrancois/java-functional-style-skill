# Review fallback laziness

Use `$java-functional-style` to create `review.md`. Assume Java 17.

Review this proposed cleanup. Keep the review concise and include a safer replacement snippet if
you recommend changes.

```java
import java.util.Map;
import java.util.Optional;

final class ProfileLookup {
    Profile profileFor(User user, Map<String, Profile> cache, RemoteProfiles remote) {
        Profile remoteProfile = remote.load(user.id());
        return Optional.ofNullable(cache.get(user.id()))
                .orElse(remoteProfile);
    }

    Profile cachedOrCreate(String id, Map<String, Profile> cache, RemoteProfiles remote) {
        Profile created = remote.load(id);
        return cache.computeIfAbsent(id, ignored -> created);
    }

    record User(String id) {}
    record Profile(String id, String displayName) {}

    interface RemoteProfiles {
        Profile load(String id);
    }
}
```

The remote call is slow and has observable rate-limit side effects. The cache may already contain
the requested profile.
