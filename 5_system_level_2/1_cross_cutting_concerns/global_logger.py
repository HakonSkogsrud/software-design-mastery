import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance")


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


class TransactionImporter(Protocol):
    def import_transactions(self) -> list[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


class CsvTransactionImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> list[Transaction]:
        logger.info("Loading transactions from %s", self.file_path)

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
        logger.info("Calling bank API")

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
        logger.info("Fetching transactions from bank API")

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


def synchronize_importer(importer: TransactionImporter) -> list[Transaction]:
    logger.info("Synchronizing %s", importer.source_name())

    if importer.supports_incremental_sync():
        logger.info("Running incremental sync")
    else:
        logger.info("Running full sync")

    transactions = importer.import_transactions()

    logger.info("Imported %s transactions", len(transactions))
    print()

    return transactions


def main() -> None:
    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
    ]

    for importer in importers:
        synchronize_importer(importer)


if __name__ == "__main__":
    main()
