from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class TransferStatus(StrEnum):
    CREATED = "created"
    COMPLETED = "completed"
    PENDING_CONFIRMATION = "pending_confirmation"


class ProviderTimeoutError(Exception):
    pass


@dataclass
class Transfer:
    id: str
    amount: Decimal
    status: TransferStatus = TransferStatus.CREATED

    def mark_as_completed(self) -> None:
        self.status = TransferStatus.COMPLETED

    def mark_as_pending_confirmation(self) -> None:
        self.status = TransferStatus.PENDING_CONFIRMATION


class PaymentProvider:
    def __init__(self) -> None:
        self._completed_transfers: set[str] = set()

    def transfer(
        self,
        *,
        transfer_id: str,
        amount: Decimal,
        idempotency_key: str,
    ) -> None:
        if idempotency_key in self._completed_transfers:
            print("Provider recognized the repeated request")
            return

        print(f"Provider transferred €{amount:.2f}")
        self._completed_transfers.add(idempotency_key)

        # The provider completed the transfer, but the response was lost.
        raise ProviderTimeoutError()

    def has_completed(self, idempotency_key: str) -> bool:
        return idempotency_key in self._completed_transfers


def submit_transfer(
    transfer: Transfer,
    provider: PaymentProvider,
) -> None:
    try:
        provider.transfer(
            transfer_id=transfer.id,
            amount=transfer.amount,
            idempotency_key=transfer.id,
        )
        transfer.mark_as_completed()
    except ProviderTimeoutError:
        transfer.mark_as_pending_confirmation()


def confirm_transfer(
    transfer: Transfer,
    provider: PaymentProvider,
) -> None:
    if provider.has_completed(transfer.id):
        transfer.mark_as_completed()


def main() -> None:
    transfer = Transfer(
        id="transfer-456",
        amount=Decimal("250.00"),
    )
    provider = PaymentProvider()

    submit_transfer(transfer, provider)

    print(f"\nStatus after timeout: {transfer.status}")
    print("The platform does not yet claim success or failure.")

    print("\nChecking the provider...")
    confirm_transfer(transfer, provider)

    print(f"Confirmed status: {transfer.status}")

    print("\nSubmitting the same request again...")
    provider.transfer(
        transfer_id=transfer.id,
        amount=transfer.amount,
        idempotency_key=transfer.id,
    )


if __name__ == "__main__":
    main()
