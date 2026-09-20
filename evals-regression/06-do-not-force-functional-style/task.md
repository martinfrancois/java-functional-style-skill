# Review proposed functional rewrite

Create `review.md`. Assume Java 17.

Review whether the proposed rewrite should be accepted.

Original:

```java
import java.util.ArrayList;
import java.util.List;

final class LogWindow {
    List<String> visibleLines(List<String> lines) {
        List<String> result = new ArrayList<>();
        boolean copying = false;
        for (String line : lines) {
            if (line.equals("--- start ---")) {
                copying = true;
                continue;
            }
            if (line.equals("--- stop ---")) {
                break;
            }
            if (copying && !line.isBlank()) {
                result.add(line.trim());
            }
        }
        return result;
    }
}
```

Proposed:

```java
import java.util.List;

final class LogWindow {
    List<String> visibleLines(List<String> lines) {
        return lines.stream()
                .filter(line -> !line.equals("--- start ---"))
                .filter(line -> !line.equals("--- stop ---"))
                .filter(line -> !line.isBlank())
                .map(String::trim)
                .toList();
    }
}
```

The method must include only nonblank lines after the start marker and before the first stop marker.
