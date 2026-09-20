# Index library loans

Create `LoanIndex.java`. Assume Java 17.

Implement these two methods in a final class `LoanIndex` and keep the nested records in the same
file:

```java
Map<String, Loan> byLoanId(List<Loan> loans)
Map<String, Loan> latestByMemberId(List<Loan> loans)
```

- `byLoanId` maps each loan's `id()` to the loan itself. If two loans share an id, keep the first
  one in encounter order. The returned map must keep encounter order.
- `latestByMemberId` maps each loan's `memberId()` to that member's loan with the latest
  `dueDate()`. If two loans of the same member have the same due date, keep the first one in
  encounter order. Encounter order of members must be preserved.

```java
record Loan(String id, String memberId, String isbn, LocalDate dueDate) {}
```

Do not add dependencies, caching, or extra public API.
