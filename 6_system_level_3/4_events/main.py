from datetime import date
from decimal import Decimal
from typing import Any

from domain.errors import NoTransactionsForPeriodError
from domain.events import TransactionCreated
from domain.models import Transaction
from domain.use_cases import create_transaction, generate_monthly_spending_report
from event_bus_adapter import InMemoryEventBus
from event_handlers import (
    refresh_budget_handler,
    send_notification_handler,
    send_webhook_handler,
)
from fastapi import FastAPI, HTTPException
from transaction_db_adapter import (
    DatabaseTransactionRepository,
    SyncDBTransactionRepository,
)

app = FastAPI()

repository = SyncDBTransactionRepository(DatabaseTransactionRepository())
event_bus = InMemoryEventBus()

event_bus.subscribe(TransactionCreated, refresh_budget_handler)
event_bus.subscribe(TransactionCreated, send_notification_handler)
event_bus.subscribe(TransactionCreated, send_webhook_handler)


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

    create_transaction(transaction, repository, event_bus)

    return {"status": "created"}


@app.get("/summary")
def get_summary_endpoint(year: int, month: int) -> dict[str, Any]:
    try:
        report = generate_monthly_spending_report(
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


@app.get("/events")
def get_events_endpoint() -> list[dict[str, Any]]:
    return [serialize_event(event) for event in event_bus.list_events()]


def serialize_event(event: object) -> dict[str, Any]:
    if isinstance(event, TransactionCreated):
        return {
            "type": "TransactionCreated",
            "transaction_id": event.transaction_id,
            "description": event.description,
            "category": event.category,
            "amount": str(event.amount),
            "currency": event.currency,
            "transaction_date": event.transaction_date.isoformat(),
            "occurred_at": event.occurred_at.isoformat(),
        }

    return {"type": type(event).__name__}
