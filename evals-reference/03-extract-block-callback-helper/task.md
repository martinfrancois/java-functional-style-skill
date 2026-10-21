# Refactor block callback

Create `EscalationReport.java`. Assume Java 17.

Refactor this class for callback readability without changing behavior:

```java
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.List;

final class EscalationReport {
    List<TicketEscalation> escalations(List<Ticket> tickets, Clock clock) {
        Instant now = Instant.now(clock);
        return tickets.stream()
                .filter(ticket -> ticket.open()
                        && ticket.assignee() != null
                        && !ticket.snoozed())
                .map(ticket -> {
                    Duration age = Duration.between(ticket.openedAt(), now);
                    String level = ticket.priority() >= 8 || age.toHours() >= 48 ? "urgent" : "normal";
                    return new TicketEscalation(ticket.id(), ticket.assignee(), level, age.toHours());
                })
                .toList();
    }

    record Ticket(String id, String assignee, int priority, Instant openedAt, boolean open, boolean snoozed) {}
    record TicketEscalation(String id, String assignee, String level, long hoursOpen) {}
}
```

Keep the same filtering and escalation rules. Do not change method signatures, records, ordering, or
clock usage.
