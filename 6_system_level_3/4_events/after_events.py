# after_event_based_architecture.py

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Protocol

from fastapi import FastAPI

app = FastAPI()


# -----------------------------
# Domain model
# -----------------------------


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


# -----------------------------
# Events
# -----------------------------


@dataclass(frozen=True)
class TransactionCreated:
    transaction_id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date
    occurred_at: datetime


EventHandler = Callable[[object], None]


class EventBus(Protocol):
    def publish(self, event: object) -> None: ...

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None: ...


class InMemoryEventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = {}
        self._published_events: list[object] = []

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        self._published_events.append(event)

        for handler in self._handlers.get(type(event), []):
            handler(event)

    def list_events(self) -> list[object]:
        return list(self._published_events)


# -----------------------------
# Port
# -----------------------------


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...

    def list_all(self) -> list[Transaction]: ...


# -----------------------------
# Application logic
# -----------------------------


def create_transaction(
    transaction: Transaction,
    repository: TransactionRepository,
    event_bus: EventBus,
) -> None:
    repository.add(transaction)

    event_bus.publish(
        TransactionCreated(
            transaction_id=transaction.id,
            description=transaction.description,
            category=transaction.category,
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_date=transaction.transaction_date,
            occurred_at=datetime.now(),
        )
    )


def calculate_total_spending(transactions: list[Transaction]) -> Decimal:
    return sum(
        (transaction.amount for transaction in transactions),
        Decimal("0.00"),
    )


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


def generate_monthly_spending_report(
    repository: TransactionRepository,
    year: int,
    month: int,
) -> SpendingReport:
    transactions = repository.list_all()
    monthly_transactions = filter_transactions_by_month(transactions, year, month)
    return generate_spending_report(monthly_transactions)


# -----------------------------
# Adapter: in-memory storage
# -----------------------------


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def list_all(self) -> list[Transaction]:
        return list(self._transactions)


# -----------------------------
# Event handlers
# -----------------------------


def update_summary_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Updating summary after transaction {event.transaction_id}")


def refresh_budget_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Refreshing budget for category {event.category}")


def send_notification_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(
        f"Sending notification: {event.description} ({event.amount} {event.currency})"
    )


def send_webhook_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Sending webhook for TransactionCreated: {event.transaction_id}")


# -----------------------------
# Composition
# -----------------------------


repository = InMemoryTransactionRepository()
event_bus = InMemoryEventBus()

event_bus.subscribe(TransactionCreated, update_summary_handler)
event_bus.subscribe(TransactionCreated, refresh_budget_handler)
event_bus.subscribe(TransactionCreated, send_notification_handler)
event_bus.subscribe(TransactionCreated, send_webhook_handler)


# -----------------------------
# Adapter: REST API
# -----------------------------


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
    report = generate_monthly_spending_report(repository, year, month)

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
    events = event_bus.list_events()

    return [serialize_event(event) for event in events]


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


# -----------------------------
# Adapter: CLI-style entry point
# -----------------------------


def print_report(report: SpendingReport) -> None:
    print()
    print("Spending report")
    print("---------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")


def run_cli_demo() -> None:
    repository = InMemoryTransactionRepository()
    event_bus = InMemoryEventBus()

    event_bus.subscribe(TransactionCreated, update_summary_handler)
    event_bus.subscribe(TransactionCreated, refresh_budget_handler)
    event_bus.subscribe(TransactionCreated, send_notification_handler)
    event_bus.subscribe(TransactionCreated, send_webhook_handler)

    create_transaction(
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("3.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        repository,
        event_bus,
    )

    create_transaction(
        Transaction(
            id="tx-002",
            description="Train ticket",
            category="Transport",
            amount=Decimal("8.75"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
        repository,
        event_bus,
    )

    report = generate_monthly_spending_report(
        repository,
        year=2026,
        month=5,
    )

    print_report(report)

    print()
    print("Event history")
    print("-------------")

    for event in event_bus.list_events():
        print(serialize_event(event))


if __name__ == "__main__":
    run_cli_demo()
