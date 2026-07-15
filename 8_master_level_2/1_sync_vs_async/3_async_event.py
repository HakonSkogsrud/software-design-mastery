from copy import copy
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from queue import Queue
from threading import Lock, Thread
from time import sleep
from typing import Any, Callable, cast
from uuid import UUID, uuid4


class TransferStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class TransferRequest:
    source_account_id: UUID
    destination_account_id: UUID
    amount: Decimal


@dataclass
class Transfer:
    id: UUID
    source_account_id: UUID
    destination_account_id: UUID
    amount: Decimal
    status: TransferStatus


@dataclass(frozen=True)
class ProcessTransfer:
    transfer_id: UUID


@dataclass(frozen=True)
class TransferCompleted:
    transfer_id: UUID
    source_account_id: UUID
    destination_account_id: UUID
    amount: Decimal


class TransferRepository:
    def __init__(self) -> None:
        self._transfers: dict[UUID, Transfer] = {}
        self._lock = Lock()

    def save(self, transfer: Transfer) -> None:
        with self._lock:
            self._transfers[transfer.id] = copy(transfer)

    def get(self, transfer_id: UUID) -> Transfer:
        with self._lock:
            return copy(self._transfers[transfer_id])


EventHandler = Callable[[Any], None]


type StoredEventHandler = Callable[[object], None]


class EventBus:
    def __init__(self) -> None:

        self._handlers: dict[
            type[object],
            list[StoredEventHandler],
        ] = {}

    def subscribe[T](
        self,
        event_type: type[T],
        handler: Callable[[T], None],
    ) -> None:

        def stored_handler(event: object) -> None:

            handler(cast(T, event))

        self._handlers.setdefault(
            event_type,
            [],
        ).append(stored_handler)

    def publish(self, event: object) -> None:

        for handler in self._handlers.get(
            type(event),
            [],
        ):
            handler(event)


class LedgerService:
    def move_funds(self, transfer: Transfer) -> None:
        print("Worker: processing transfer...")
        sleep(2)

        print(
            f"Worker: moved {transfer.amount} from "
            f"{transfer.source_account_id} to "
            f"{transfer.destination_account_id}"
        )


class NotificationService:
    def send_confirmation(self, transfer_id: UUID) -> None:
        print(f"Notification handler: sent confirmation for transfer {transfer_id}")


class PortfolioService:
    def refresh_positions(self, account_id: UUID) -> None:
        print(f"Portfolio handler: refreshed positions for account {account_id}")


transfer_repository = TransferRepository()
transfer_queue: Queue[ProcessTransfer | None] = Queue()

event_bus = EventBus()
ledger_service = LedgerService()
notification_service = NotificationService()
portfolio_service = PortfolioService()


def request_transfer(request: TransferRequest) -> Transfer:
    transfer = Transfer(
        id=uuid4(),
        source_account_id=request.source_account_id,
        destination_account_id=request.destination_account_id,
        amount=request.amount,
        status=TransferStatus.PENDING,
    )

    transfer_repository.save(transfer)

    transfer_queue.put(ProcessTransfer(transfer_id=transfer.id))

    return transfer


def transfer_worker() -> None:
    while True:
        message = transfer_queue.get()

        if message is None:
            transfer_queue.task_done()
            return

        transfer = transfer_repository.get(message.transfer_id)

        try:
            ledger_service.move_funds(transfer)
        except Exception:
            transfer.status = TransferStatus.FAILED
            transfer_repository.save(transfer)
        else:
            transfer.status = TransferStatus.COMPLETED
            transfer_repository.save(transfer)

            event_bus.publish(
                TransferCompleted(
                    transfer_id=transfer.id,
                    source_account_id=transfer.source_account_id,
                    destination_account_id=transfer.destination_account_id,
                    amount=transfer.amount,
                )
            )

        transfer_queue.task_done()


def send_transfer_confirmation(
    event: TransferCompleted,
) -> None:
    notification_service.send_confirmation(event.transfer_id)


def refresh_portfolios(
    event: TransferCompleted,
) -> None:
    portfolio_service.refresh_positions(event.source_account_id)
    portfolio_service.refresh_positions(event.destination_account_id)


event_bus.subscribe(
    TransferCompleted,
    send_transfer_confirmation,
)

event_bus.subscribe(
    TransferCompleted,
    refresh_portfolios,
)


def main() -> None:
    worker = Thread(
        target=transfer_worker,
        daemon=True,
    )
    worker.start()

    request = TransferRequest(
        source_account_id=uuid4(),
        destination_account_id=uuid4(),
        amount=Decimal("250.00"),
    )

    transfer = request_transfer(request)

    print(f"Request: transfer returned immediately with status {transfer.status}")

    sleep(0.5)

    current_transfer = transfer_repository.get(transfer.id)

    print(f"Request: transfer is still {current_transfer.status}")

    transfer_queue.join()

    completed_transfer = transfer_repository.get(transfer.id)

    print(f"Later: transfer is now {completed_transfer.status}")

    transfer_queue.put(None)
    worker.join()


if __name__ == "__main__":
    main()
