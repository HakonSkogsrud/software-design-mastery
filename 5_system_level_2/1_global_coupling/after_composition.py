# after_composition.py

import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable, Protocol


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


class Logger(Protocol):
    def info(self, message: str, *args: object) -> None: ...


class TransactionImporter(Protocol):
    def import_transactions(self) -> Iterable[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


class CsvTransactionImporter:
    def __init__(self, file_path: str, logger: Logger) -> None:
        self.file_path = file_path
        self.logger = logger

    def import_transactions(self) -> Iterable[Transaction]:
        self.logger.info("Streaming transactions from %s", self.file_path)

        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                yield Transaction(
                    id=row["id"],
                    description=row["description"],
                    category=row["category"],
                    amount=Decimal(row["amount"]),
                    currency=row["currency"],
                    transaction_date=date.fromisoformat(row["transaction_date"]),
                )

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"


class BankApiClient:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def fetch_transactions(self) -> list[dict[str, str]]:
        self.logger.info("Calling bank API")

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
    def __init__(self, api_client: BankApiClient, logger: Logger) -> None:
        self.api_client = api_client
        self.logger = logger

    def import_transactions(self) -> Iterable[Transaction]:
        self.logger.info("Fetching transactions from bank API")

        payload = self.api_client.fetch_transactions()

        for item in payload:
            yield Transaction(
                id=item["transaction_id"],
                description=item["details"],
                category=item["type"],
                amount=Decimal(item["value"]),
                currency=item["currency_code"],
                transaction_date=date.fromisoformat(item["date_posted"]),
            )

    def supports_incremental_sync(self) -> bool:
        return True

    def source_name(self) -> str:
        return "bank_api"


class TransactionSynchronizer:
    def __init__(
        self,
        currency: str,
        logger: Logger,
    ) -> None:
        self.currency = currency
        self.logger = logger

    def synchronize(self, importer: TransactionImporter) -> None:
        self.logger.info("Synchronizing %s", importer.source_name())

        if importer.supports_incremental_sync():
            self.logger.info("Running incremental sync")
        else:
            self.logger.info("Running full sync")

        transactions = importer.import_transactions()
        transactions = self._filter_by_currency(transactions)

        transaction_count = 0

        for transaction in transactions:
            print(transaction)
            transaction_count += 1

        self.logger.info("Imported %s transactions", transaction_count)
        print()

    def _filter_by_currency(
        self,
        transactions: Iterable[Transaction],
    ) -> Iterable[Transaction]:
        self.logger.info("Filtering transactions by currency: %s", self.currency)

        for transaction in transactions:
            if transaction.currency == self.currency:
                yield transaction


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    logger = create_logger()

    api_client = BankApiClient(logger)

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv", logger),
        BankApiImporter(api_client, logger),
    ]

    synchronizer = TransactionSynchronizer(
        currency="EUR",
        logger=logger,
    )

    for importer in importers:
        synchronizer.synchronize(importer)


if __name__ == "__main__":
    main()
