# partial_application.py

import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from functools import partial
from typing import Callable, Protocol


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


class Logger(Protocol):
    def info(self, msg: object, *args: object) -> None: ...


class TransactionImporter(Protocol):
    def import_transactions(self) -> list[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


type TransactionFilter = Callable[[list[Transaction]], list[Transaction]]


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


def filter_by_currency(
    transactions: list[Transaction],
    currency: str,
    logger: Logger,
) -> list[Transaction]:
    logger.info("Filtering transactions by currency: %s", currency)

    return [
        transaction for transaction in transactions if transaction.currency == currency
    ]


class TransactionSynchronizer:
    def __init__(
        self,
        transaction_filter: TransactionFilter,
        logger: Logger,
    ) -> None:
        self.transaction_filter = transaction_filter
        self.logger = logger

    def synchronize(
        self,
        importer: TransactionImporter,
    ) -> list[Transaction]:
        self.logger.info("Synchronizing %s", importer.source_name())

        transactions = importer.import_transactions()
        transactions = self.transaction_filter(transactions)

        self.logger.info("Imported %s transactions", len(transactions))
        print()

        return transactions


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    logger = create_logger()

    eur_filter = partial(
        filter_by_currency,
        currency="EUR",
        logger=logger,
    )

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
    ]

    synchronizer = TransactionSynchronizer(
        transaction_filter=eur_filter,
        logger=logger,
    )

    for importer in importers:
        synchronizer.synchronize(importer)


if __name__ == "__main__":
    main()
