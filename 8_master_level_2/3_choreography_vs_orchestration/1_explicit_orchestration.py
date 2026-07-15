from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    description: str
    category: str
    amount: Decimal
    transaction_date: date


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int


class NoTransactionsForPeriodError(Exception):
    pass


def generate_monthly_spending_report(
    transactions: list[Transaction],
    year: int,
    month: int,
) -> SpendingReport:
    monthly_transactions = [
        transaction
        for transaction in transactions
        if transaction.transaction_date.year == year
        and transaction.transaction_date.month == month
    ]

    if not monthly_transactions:
        raise NoTransactionsForPeriodError(
            f"No transactions found for {year}-{month:02d}"
        )

    total_spent = sum(
        (transaction.amount for transaction in monthly_transactions),
        start=Decimal("0"),
    )

    totals_by_category: dict[str, Decimal] = {}

    for transaction in monthly_transactions:
        totals_by_category[transaction.category] = (
            totals_by_category.get(transaction.category, Decimal("0"))
            + transaction.amount
        )

    return SpendingReport(
        total_spent=total_spent,
        totals_by_category=totals_by_category,
        transaction_count=len(monthly_transactions),
    )


def main() -> None:
    transactions = [
        Transaction(
            description="Groceries",
            category="food",
            amount=Decimal("42.50"),
            transaction_date=date(2026, 7, 3),
        ),
        Transaction(
            description="Train ticket",
            category="travel",
            amount=Decimal("18.20"),
            transaction_date=date(2026, 7, 5),
        ),
        Transaction(
            description="Restaurant",
            category="food",
            amount=Decimal("35.00"),
            transaction_date=date(2026, 6, 28),
        ),
    ]

    report = generate_monthly_spending_report(
        transactions,
        year=2026,
        month=7,
    )

    print(report)


if __name__ == "__main__":
    main()
