# Order volunteer shifts

Create `ShiftOrdering.java`. Assume Java 17.

Clean up the comparator in this class without changing the resulting order:

```java
import java.time.DayOfWeek;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

final class ShiftOrdering {
    List<Shift> ordered(List<Shift> shifts) {
        List<Shift> copy = new ArrayList<>(shifts);
        copy.sort((a, b) -> {
            int byDay = a.day().compareTo(b.day());
            if (byDay != 0) {
                return byDay;
            }
            int byStart = a.start().compareTo(b.start());
            if (byStart != 0) {
                return byStart;
            }
            if (a.lead() == null && b.lead() == null) {
                return 0;
            }
            if (a.lead() == null) {
                return 1;
            }
            if (b.lead() == null) {
                return -1;
            }
            int byLead = a.lead().compareTo(b.lead());
            if (byLead != 0) {
                return byLead;
            }
            return Integer.compare(a.slots(), b.slots());
        });
        return copy;
    }

    record Shift(DayOfWeek day, LocalTime start, String lead, int slots) {}
}
```

Keep the method signature and the nested record. Shifts without a lead must still sort after
shifts with a lead on the same day and start time.
