# before_api_coupled.py

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import FastAPI

app = FastAPI()


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


transactions: list[Transaction] = []


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
        totals.setdefault(transaction.category, Decimal("0.00"))
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


@app.post("/transactions")
def create_transaction(request: dict[str, Any]) -> dict[str, str]:
    transaction = Transaction(
        id=request["id"],
        description=request["description"],
        category=request["category"],
        amount=Decimal(request["amount"]),
        currency=request["currency"],
        transaction_date=date.fromisoformat(request["transaction_date"]),
    )

    transactions.append(transaction)

    return {"status": "created"}


@app.get("/summary")
def get_summary(year: int, month: int) -> dict[str, Any]:
    monthly_transactions = filter_transactions_by_month(
        transactions,
        year=year,
        month=month,
    )

    report = generate_spending_report(monthly_transactions)

    return {
        "total_spent": str(report.total_spent),
        "transaction_count": report.transaction_count,
        "totals_by_category": {
            category: str(total)
            for category, total in report.totals_by_category.items()
        },
    }
