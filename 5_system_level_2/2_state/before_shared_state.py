# before_shared_state.py

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


monthly_totals: dict[str, Decimal] = {}
account_balance = Decimal("0.00")


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


def filter_by_currency(
    transactions: Iterable[Transaction],
    currency: str,
    logger: Logger,
) -> Iterable[Transaction]:
    logger.info("Filtering transactions by currency: %s", currency)

    for transaction in transactions:
        if transaction.currency == currency:
            yield transaction


def synchronize_importer(
    importer: TransactionImporter,
    logger: Logger,
) -> None:
    global account_balance

    logger.info("Synchronizing %s", importer.source_name())

    transactions = importer.import_transactions()
    transactions = filter_by_currency(transactions, "EUR", logger)

    transaction_count = 0

    for transaction in transactions:
        print(transaction)

        account_balance += transaction.amount

        current_total = monthly_totals.get(
            transaction.category,
            Decimal("0.00"),
        )
        monthly_totals[transaction.category] = current_total + transaction.amount

        transaction_count += 1

    logger.info("Imported %s transactions", transaction_count)
    print()


def print_summary() -> None:
    print("Spending summary")
    print("----------------")
    print(f"Account balance: €{account_balance}")
    print()

    for category, total in monthly_totals.items():
        print(f"- {category}: €{total}")


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

    for importer in importers:
        synchronize_importer(importer, logger)

    print_summary()


if __name__ == "__main__":
    main()
