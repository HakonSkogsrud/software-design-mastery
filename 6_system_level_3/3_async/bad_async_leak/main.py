from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import FastAPI, HTTPException

from .domain.errors import NoTransactionsForPeriodError
from .domain.models import Transaction
from .domain.use_cases import create_transaction, generate_monthly_spending_report
from .transaction_db_adapter import DatabaseTransactionRepository

app = FastAPI()

repository = DatabaseTransactionRepository()


@app.post("/transactions")
async def create_transaction_endpoint(request: dict[str, Any]) -> dict[str, str]:
    transaction = Transaction(
        id=request["id"],
        description=request["description"],
        category=request["category"],
        amount=Decimal(request["amount"]),
        currency=request["currency"],
        transaction_date=date.fromisoformat(request["transaction_date"]),
    )

    await create_transaction(transaction, repository)

    return {"status": "created"}


@app.get("/summary")
async def get_summary_endpoint(year: int, month: int) -> dict[str, Any]:
    try:
        report = await generate_monthly_spending_report(
            repository,
            year=year,
            month=month,
        )
    except NoTransactionsForPeriodError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return {
        "total_spent": str(report.total_spent),
        "transaction_count": report.transaction_count,
        "totals_by_category": {
            category: str(total)
            for category, total in report.totals_by_category.items()
        },
    }
