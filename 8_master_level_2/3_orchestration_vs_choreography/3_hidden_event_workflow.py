from dataclasses import dataclass
from typing import Callable

type EventHandler = Callable[[object], None]


@dataclass(frozen=True)
class TransactionSubmitted:
    transaction_id: str


@dataclass(frozen=True)
class TransactionValidated:
    transaction_id: str


@dataclass(frozen=True)
class DuplicateCheckPassed:
    transaction_id: str


@dataclass(frozen=True)
class FraudCheckPassed:
    transaction_id: str


@dataclass(frozen=True)
class TransactionCreated:
    transaction_id: str


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
        print(f"Published: {type(event).__name__}")

        for handler in self._handlers.get(type(event), []):
            handler(event)


event_bus = InMemoryEventBus()


def validate_transaction_handler(event: object) -> None:
    if not isinstance(event, TransactionSubmitted):
        return

    print("Validating transaction")

    event_bus.publish(
        TransactionValidated(
            transaction_id=event.transaction_id,
        )
    )


def check_duplicate_handler(event: object) -> None:
    if not isinstance(event, TransactionValidated):
        return

    print("Checking for duplicates")

    event_bus.publish(
        DuplicateCheckPassed(
            transaction_id=event.transaction_id,
        )
    )


def check_fraud_handler(event: object) -> None:
    if not isinstance(event, DuplicateCheckPassed):
        return

    print("Running fraud checks")

    event_bus.publish(
        FraudCheckPassed(
            transaction_id=event.transaction_id,
        )
    )


def create_transaction_handler(event: object) -> None:
    if not isinstance(event, FraudCheckPassed):
        return

    print("Creating transaction")

    event_bus.publish(
        TransactionCreated(
            transaction_id=event.transaction_id,
        )
    )


def send_notification_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print("Sending notification")


def main() -> None:
    event_bus.subscribe(
        TransactionSubmitted,
        validate_transaction_handler,
    )
    event_bus.subscribe(
        TransactionValidated,
        check_duplicate_handler,
    )
    event_bus.subscribe(
        DuplicateCheckPassed,
        check_fraud_handler,
    )
    event_bus.subscribe(
        FraudCheckPassed,
        create_transaction_handler,
    )
    event_bus.subscribe(
        TransactionCreated,
        send_notification_handler,
    )

    event_bus.publish(
        TransactionSubmitted(
            transaction_id="tx-001",
        )
    )


if __name__ == "__main__":
    main()
