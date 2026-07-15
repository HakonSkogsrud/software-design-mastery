from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(frozen=True)
class TransferRequest:
    source_account_id: UUID
    destination_account_id: UUID
    amount: Decimal


@dataclass(frozen=True)
class Transfer:
    id: UUID
    source_account_id: UUID
    destination_account_id: UUID
    amount: Decimal


class TransferService:
    def transfer(self, request: TransferRequest) -> Transfer:
        print(
            f"Moving {request.amount} from "
            f"{request.source_account_id} to "
            f"{request.destination_account_id}"
        )

        return Transfer(
            id=uuid4(),
            source_account_id=request.source_account_id,
            destination_account_id=request.destination_account_id,
            amount=request.amount,
        )


class NotificationService:
    def send_confirmation(self, transfer: Transfer) -> None:
        print(f"Sending confirmation for transfer {transfer.id}")


class PortfolioService:
    def refresh_positions(self, account_id: UUID) -> None:
        print(f"Refreshing portfolio for account {account_id}")


transfer_service = TransferService()
notification_service = NotificationService()
portfolio_service = PortfolioService()


def transfer_money(request: TransferRequest) -> Transfer:
    transfer = transfer_service.transfer(request)

    notification_service.send_confirmation(transfer)

    portfolio_service.refresh_positions(transfer.source_account_id)
    portfolio_service.refresh_positions(transfer.destination_account_id)

    return transfer


def main() -> None:
    request = TransferRequest(
        source_account_id=uuid4(),
        destination_account_id=uuid4(),
        amount=Decimal("250.00"),
    )

    transfer = transfer_money(request)

    print(f"Transfer {transfer.id} completed")


if __name__ == "__main__":
    main()
