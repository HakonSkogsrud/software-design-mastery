from datetime import date
from decimal import Decimal

from models import MonthlySummary, Transaction, TransactionType


def generate_monthly_summary(
    transactions: list[Transaction],
    *,
    month: int,
    year: int,
) -> MonthlySummary:
    monthly_transactions = [
        transaction
        for transaction in transactions
        if transaction.booked_at.month == month and transaction.booked_at.year == year
    ]

    total_income = sum(
        transaction.amount
        for transaction in monthly_transactions
        if transaction.transaction_type == TransactionType.INCOME
    )

    total_expenses = sum(
        transaction.amount
        for transaction in monthly_transactions
        if transaction.transaction_type == TransactionType.EXPENSE
    )

    return MonthlySummary(
        month=month,
        year=year,
        total_income=total_income,
        total_expenses=total_expenses,
    )


def main() -> None:
    transactions = [
        Transaction(
            "Salary",
            Decimal("4000"),
            TransactionType.INCOME,
            date(2026, 6, 1),
        ),
        Transaction(
            "Rent",
            Decimal("1500"),
            TransactionType.EXPENSE,
            date(2026, 6, 3),
        ),
        Transaction(
            "Groceries",
            Decimal("280"),
            TransactionType.EXPENSE,
            date(2026, 6, 12),
        ),
    ]

    summary = generate_monthly_summary(
        transactions,
        month=6,
        year=2026,
    )

    print(summary)


if __name__ == "__main__":
    main()
