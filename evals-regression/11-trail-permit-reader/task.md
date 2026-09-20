# Trail permit files

Create `PermitFiles.java`. Assume Java 17.

Implement a final class `PermitFiles` with this method and keep the nested record and the
provided parser in the same file:

```java
List<Permit> readPermits(List<Path> files) throws IOException
```

Read each file with `Files.readString`, parse it with the provided `parse` method, and return the
permits in the same order as the files. An `IOException` from reading must propagate to the caller
as an `IOException`; an `IllegalArgumentException` from parsing must propagate unchanged.

```java
record Permit(String trail, String holder) {}

private static Permit parse(String raw) {
    String[] parts = raw.strip().split(";");
    if (parts.length != 2) {
        throw new IllegalArgumentException("expected trail;holder but got: " + raw);
    }
    return new Permit(parts[0], parts[1]);
}
```

Do not add dependencies or extra public API.
