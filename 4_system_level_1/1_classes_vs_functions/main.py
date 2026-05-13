from dataclasses import dataclass
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
        if transaction.category not in totals:
            totals[transaction.category] = Decimal("0.00")

        totals[transaction.category] += transaction.amount

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


def print_report(report: SpendingReport) -> None:
    print("Spending report")
    print("---------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    print("By category:")
    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")


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
    ]


def main() -> None:
    transactions = load_transactions()

    may_transactions = filter_transactions_by_month(
        transactions,
        year=2026,
        month=5,
    )

    report = generate_spending_report(may_transactions)

    print_report(report)


if __name__ == "__main__":
    main()
