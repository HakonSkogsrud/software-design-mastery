# derived_state.py

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


def calculate_balance(transactions: list[Transaction]) -> Decimal:
    return sum(
        (transaction.amount for transaction in transactions),
        Decimal("0.00"),
    )


def calculate_totals_by_category(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        current_total = totals.get(transaction.category, Decimal("0.00"))
        totals[transaction.category] = current_total + transaction.amount

    return totals


def print_report(transactions: list[Transaction]) -> None:
    balance = calculate_balance(transactions)
    totals_by_category = calculate_totals_by_category(transactions)

    print("Derived report")
    print("--------------")
    print(f"Balance: €{balance}")
    print(f"Transactions: {len(transactions)}")
    print()

    for category, total in totals_by_category.items():
        print(f"- {category}: €{total}")


def main() -> None:
    transactions = [
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("-3.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        Transaction(
            id="tx-002",
            description="Salary",
            category="Income",
            amount=Decimal("2500.00"),
            currency="EUR",
            transaction_date=date(2026, 5, 2),
        ),
        Transaction(
            id="tx-003",
            description="Train ticket",
            category="Transport",
            amount=Decimal("-8.75"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
    ]

    print_report(transactions)


if __name__ == "__main__":
    main()
