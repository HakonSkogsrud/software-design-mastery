from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Callable, Protocol

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
            occurred_at=datetime.now(),
        )


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...

    def exists(self, transaction_id: str) -> bool: ...


class EventBus(Protocol):
    def publish(self, event: object) -> None: ...


class TransactionValidator(Protocol):
    def validate(self, transaction: Transaction) -> None: ...


class FraudChecker(Protocol):
    def check(self, transaction: Transaction) -> None: ...


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: dict[str, Transaction] = {}

    def add(self, transaction: Transaction) -> None:
        self._transactions[transaction.id] = transaction

    def exists(self, transaction_id: str) -> bool:
        return transaction_id in self._transactions


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


class BasicTransactionValidator:
    def validate(self, transaction: Transaction) -> None:
        if not transaction.description.strip():
            raise ValueError("Description cannot be empty")

        if transaction.amount <= 0:
            raise ValueError("Amount must be positive")

        if len(transaction.currency) != 3:
            raise ValueError("Currency must contain three characters")


class SimpleFraudChecker:
    def check(self, transaction: Transaction) -> None:
        if transaction.amount >= Decimal("10000"):
            raise ValueError("Transaction requires manual review")


class TransactionImportWorkflow:
    def __init__(
        self,
        repository: TransactionRepository,
        validator: TransactionValidator,
        fraud_checker: FraudChecker,
        event_bus: EventBus,
    ) -> None:
        self.repository = repository
        self.validator = validator
        self.fraud_checker = fraud_checker
        self.event_bus = event_bus

    def execute(self, transaction: Transaction) -> None:
        self.validator.validate(transaction)

        if self.repository.exists(transaction.id):
            raise ValueError(f"Transaction {transaction.id} already exists")

        self.fraud_checker.check(transaction)
        self.repository.add(transaction)

        self.event_bus.publish(TransactionCreated.from_transaction(transaction))


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


def main() -> None:
    repository = InMemoryTransactionRepository()
    event_bus = InMemoryEventBus()

    event_bus.subscribe(TransactionCreated, refresh_budget_handler)
    event_bus.subscribe(TransactionCreated, send_notification_handler)
    event_bus.subscribe(TransactionCreated, send_webhook_handler)

    workflow = TransactionImportWorkflow(
        repository=repository,
        validator=BasicTransactionValidator(),
        fraud_checker=SimpleFraudChecker(),
        event_bus=event_bus,
    )

    transaction = Transaction(
        id="tx-001",
        description="Groceries",
        category="food",
        amount=Decimal("42.50"),
        currency="EUR",
        transaction_date=date(2026, 7, 15),
    )

    workflow.execute(transaction)


if __name__ == "__main__":
    main()
