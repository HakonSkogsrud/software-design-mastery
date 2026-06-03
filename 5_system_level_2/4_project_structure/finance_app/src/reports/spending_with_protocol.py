from decimal import Decimal
from typing import Protocol

from .models import SpendingReport


class Transaction(Protocol):
    category: str
    amount: Decimal


def calculate_total_spending(
    transactions: list[Transaction],
) -> Decimal:
    total = Decimal("0.00")

    for transaction in transactions:
        total += transaction.amount

    return total


def calculate_spending_by_category(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        totals.setdefault(transaction.category, Decimal("0.00"))
        totals[transaction.category] += transaction.amount

    return totals


def generate_spending_report(
    transactions: list[Transaction],
) -> SpendingReport:
    return SpendingReport(
        total_spent=calculate_total_spending(transactions),
        totals_by_category=calculate_spending_by_category(transactions),
        transaction_count=len(transactions),
    )
