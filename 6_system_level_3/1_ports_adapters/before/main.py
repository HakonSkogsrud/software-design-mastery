from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import FastAPI, HTTPException

from .domain.models import SpendingReport, Transaction
from .domain.transaction_logic import (
    calculate_spending_by_category,
    calculate_total_spending,
    filter_transactions_by_month,
)

app = FastAPI()

transactions: list[Transaction] = []


@app.post("/transactions")
def create_transaction_endpoint(request: dict[str, Any]) -> dict[str, str]:
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
def get_summary_endpoint(year: int, month: int) -> dict[str, Any]:
    monthly_transactions = filter_transactions_by_month(
        transactions,
        year=year,
        month=month,
    )

    if not monthly_transactions:
        raise HTTPException(
            status_code=404, detail=f"No transactions found for {year}-{month:02d}"
        )

    report = SpendingReport(
        total_spent=calculate_total_spending(monthly_transactions),
        totals_by_category=calculate_spending_by_category(monthly_transactions),
        transaction_count=len(monthly_transactions),
    )

    return {
        "total_spent": str(report.total_spent),
        "transaction_count": report.transaction_count,
        "totals_by_category": {
            category: str(total)
            for category, total in report.totals_by_category.items()
        },
    }
