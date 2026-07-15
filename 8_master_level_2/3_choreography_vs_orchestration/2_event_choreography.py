from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Callable

type EventHandler = Callable[[object], None]


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


@dataclass(frozen=True)
class TransactionCreated:
    transaction_id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date
    occurred_at: datetime

    @classmethod
    def from_transaction(
        cls,
        transaction: Transaction,
    ) -> "TransactionCreated":
        return cls(
            transaction_id=transaction.id,
            description=transaction.description,
            category=transaction.category,
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_date=transaction.transaction_date,
            occurred_at=datetime.now(),
        )


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)


class InMemoryEventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)


def refresh_budget_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Refreshing budget for category: {event.category}")


def send_notification_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(
        f"Sending notification: {event.description} ({event.amount} {event.currency})"
    )


def send_webhook_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Sending webhook for transaction: {event.transaction_id}")


def create_transaction(
    transaction: Transaction,
    repository: InMemoryTransactionRepository,
    event_bus: InMemoryEventBus,
) -> None:
    repository.add(transaction)
    event_bus.publish(TransactionCreated.from_transaction(transaction))


def main() -> None:
    repository = InMemoryTransactionRepository()
    event_bus = InMemoryEventBus()

    event_bus.subscribe(TransactionCreated, refresh_budget_handler)
    event_bus.subscribe(TransactionCreated, send_notification_handler)
    event_bus.subscribe(TransactionCreated, send_webhook_handler)

    transaction = Transaction(
        id="tx-001",
        description="Groceries",
        category="food",
        amount=Decimal("42.50"),
        currency="EUR",
        transaction_date=date(2026, 7, 15),
    )

    create_transaction(transaction, repository, event_bus)


if __name__ == "__main__":
    main()
