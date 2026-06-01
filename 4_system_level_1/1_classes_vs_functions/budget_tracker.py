from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int


@dataclass
class BudgetTracker:
    monthly_limits: dict[str, Decimal]
    monthly_totals: dict[str, Decimal] = field(default_factory=dict[str, Decimal])

    def add_transaction(self, transaction: Transaction) -> None:
        current_total = self.monthly_totals.get(
            transaction.category,
            Decimal("0.00"),
        )

        self.monthly_totals[transaction.category] = current_total + transaction.amount

    def total_for_category(self, category: str) -> Decimal:
        return self.monthly_totals.get(category, Decimal("0.00"))

    def limit_for_category(self, category: str) -> Decimal | None:
        return self.monthly_limits.get(category)

    def is_over_limit(self, category: str) -> bool:
        limit = self.limit_for_category(category)

        if limit is None:
            return False

        return self.total_for_category(category) > limit

    def overspent_categories(self) -> list[str]:
        return [
            category for category in self.monthly_totals if self.is_over_limit(category)
        ]


def calculate_total_spending(transactions: list[Transaction]) -> Decimal:
    total = Decimal("0.00")

    for transaction in transactions:
        total += transaction.amount

    return total


def calculate_spending_by_category(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        current_total = totals.get(transaction.category, Decimal("0.00"))
        totals[transaction.category] = current_total + transaction.amount

    return totals


def filter_transactions_by_month(
    transactions: list[Transaction],
    year: int,
    month: int,
) -> list[Transaction]:
    return [
        transaction
        for transaction in transactions
        if transaction.transaction_date.year == year
        and transaction.transaction_date.month == month
    ]


def generate_spending_report(
    transactions: list[Transaction],
) -> SpendingReport:
    return SpendingReport(
        total_spent=calculate_total_spending(transactions),
        totals_by_category=calculate_spending_by_category(transactions),
        transaction_count=len(transactions),
    )


def build_budget_tracker(
    transactions: list[Transaction],
    monthly_limits: dict[str, Decimal],
) -> BudgetTracker:
    tracker = BudgetTracker(monthly_limits)

    for transaction in transactions:
        tracker.add_transaction(transaction)

    return tracker


def print_report(report: SpendingReport) -> None:
    print("Spending report")
    print("---------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    print("By category:")
    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")


def print_budget_status(tracker: BudgetTracker) -> None:
    print()
    print("Budget status")
    print("-------------")

    for category, total in tracker.monthly_totals.items():
        limit = tracker.limit_for_category(category)

        if limit is None:
            print(f"- {category}: €{total} / no limit")
            continue

        status = "OVER LIMIT" if tracker.is_over_limit(category) else "OK"
        print(f"- {category}: €{total} / €{limit} ({status})")


def load_transactions() -> list[Transaction]:
    return [
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("3.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        Transaction(
            id="tx-002",
            description="Groceries",
            category="Food",
            amount=Decimal("42.10"),
            currency="EUR",
            transaction_date=date(2026, 5, 3),
        ),
        Transaction(
            id="tx-003",
            description="Train ticket",
            category="Transport",
            amount=Decimal("8.75"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
        Transaction(
            id="tx-004",
            description="Book",
            category="Education",
            amount=Decimal("19.99"),
            currency="EUR",
            transaction_date=date(2026, 5, 6),
        ),
        Transaction(
            id="tx-005",
            description="Restaurant",
            category="Food",
            amount=Decimal("36.40"),
            currency="EUR",
            transaction_date=date(2026, 4, 28),
        ),
        Transaction(
            id="tx-006",
            description="Dinner",
            category="Food",
            amount=Decimal("27.80"),
            currency="EUR",
            transaction_date=date(2026, 5, 8),
        ),
    ]


def main() -> None:
    transactions = load_transactions()

    may_transactions = filter_transactions_by_month(
        transactions,
        year=2026,
        month=5,
    )

    report = generate_spending_report(may_transactions)

    monthly_limits = {
        "Food": Decimal("70.00"),
        "Transport": Decimal("25.00"),
        "Education": Decimal("50.00"),
    }

    tracker = build_budget_tracker(
        may_transactions,
        monthly_limits,
    )

    print_report(report)
    print_budget_status(tracker)


if __name__ == "__main__":
    main()
