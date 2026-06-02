import csv
import logging
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


@dataclass
class AccountSnapshot:
    balance: Decimal = Decimal("0.00")
    totals_by_category: dict[str, Decimal] = field(default_factory=dict[str, Decimal])
    transaction_count: int = 0


class Logger(Protocol):
    def info(self, msg: object, *args: object) -> None: ...


class TransactionImporter(Protocol):
    def import_transactions(self) -> list[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


class CsvTransactionImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> list[Transaction]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            return [
                Transaction(
                    id=row["id"],
                    description=row["description"],
                    category=row["category"],
                    amount=Decimal(row["amount"]),
                    currency=row["currency"],
                    transaction_date=date.fromisoformat(row["transaction_date"]),
                )
                for row in reader
            ]

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"


class BankApiClient:
    def fetch_transactions(self) -> list[dict[str, str]]:
        return [
            {
                "transaction_id": "bank-001",
                "details": "Salary",
                "type": "Income",
                "value": "2500.00",
                "currency_code": "EUR",
                "date_posted": "2026-05-02",
            }
        ]


class BankApiImporter:
    def __init__(self, api_client: BankApiClient) -> None:
        self.api_client = api_client

    def import_transactions(self) -> list[Transaction]:
        payload = self.api_client.fetch_transactions()

        return [
            Transaction(
                id=item["transaction_id"],
                description=item["details"],
                category=item["type"],
                amount=Decimal(item["value"]),
                currency=item["currency_code"],
                transaction_date=date.fromisoformat(item["date_posted"]),
            )
            for item in payload
        ]

    def supports_incremental_sync(self) -> bool:
        return True

    def source_name(self) -> str:
        return "bank_api"


class TransactionSynchronizer:
    def __init__(
        self,
        snapshot: AccountSnapshot,
        logger: Logger,
    ) -> None:
        self.snapshot = snapshot
        self.logger = logger

    def synchronize(
        self,
        importer: TransactionImporter,
    ) -> list[Transaction]:
        self.logger.info("Synchronizing %s", importer.source_name())

        transactions = importer.import_transactions()

        for transaction in transactions:
            self.snapshot.balance += transaction.amount
            self.snapshot.transaction_count += 1

            current_total = self.snapshot.totals_by_category.get(
                transaction.category,
                Decimal("0.00"),
            )
            self.snapshot.totals_by_category[transaction.category] = (
                current_total + transaction.amount
            )

        self.logger.info("Imported %s transactions", len(transactions))
        return transactions


def print_snapshot(snapshot: AccountSnapshot) -> None:
    print("Account snapshot")
    print("----------------")
    print(f"Balance: €{snapshot.balance}")
    print(f"Transactions: {snapshot.transaction_count}")
    print()

    for category, total in snapshot.totals_by_category.items():
        print(f"- {category}: €{total}")


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    snapshot = AccountSnapshot()

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
    ]

    synchronizer = TransactionSynchronizer(
        snapshot=snapshot,
        logger=create_logger(),
    )

    for importer in importers:
        synchronizer.synchronize(importer)

    print_snapshot(snapshot)


if __name__ == "__main__":
    main()
