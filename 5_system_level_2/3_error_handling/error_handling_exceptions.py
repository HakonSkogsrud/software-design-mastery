# error_handling_exceptions.py

import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Protocol


class FinanceError(Exception):
    pass


class TransactionImportError(FinanceError):
    pass


class InvalidTransactionError(TransactionImportError):
    pass


class UnsupportedCurrencyError(TransactionImportError):
    pass


class BankApiError(TransactionImportError):
    pass


SUPPORTED_CURRENCIES = {"EUR", "USD"}


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date

    def __post_init__(self) -> None:
        if self.amount <= Decimal("0.00"):
            raise InvalidTransactionError(
                f"Transaction amount must be positive: {self.amount}"
            )

        if self.currency not in SUPPORTED_CURRENCIES:
            raise UnsupportedCurrencyError(f"Unsupported currency: {self.currency}")


class Logger(Protocol):
    def info(self, msg: object, *args: object) -> None: ...

    def error(self, msg: object, *args: object) -> None: ...


class TransactionImporter(Protocol):
    def import_transactions(self) -> list[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


class CsvTransactionImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> list[Transaction]:
        try:
            with open(self.file_path, newline="") as csv_file:
                reader = csv.DictReader(csv_file)

                return [
                    self._parse_transaction(row, line_number)
                    for line_number, row in enumerate(reader, start=2)
                ]

        except OSError as error:
            raise TransactionImportError(
                f"Could not open transaction file: {self.file_path}"
            ) from error

    def _parse_transaction(
        self,
        row: dict[str, str],
        line_number: int,
    ) -> Transaction:
        try:
            return Transaction(
                id=row["id"],
                description=row["description"],
                category=row["category"],
                amount=Decimal(row["amount"]),
                currency=row["currency"],
                transaction_date=date.fromisoformat(row["transaction_date"]),
            )

        except KeyError as error:
            raise InvalidTransactionError(
                f"Missing field {error} on line {line_number}"
            ) from error

        except InvalidOperation as error:
            raise InvalidTransactionError(
                f"Invalid amount on line {line_number}: {row.get('amount')}"
            ) from error

        except ValueError as error:
            raise InvalidTransactionError(
                f"Invalid date on line {line_number}: {row.get('transaction_date')}"
            ) from error

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"


class BankApiClient:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail

    def fetch_transactions(self) -> list[dict[str, str]]:
        if self.should_fail:
            raise ConnectionError("Bank API is unavailable")

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
        try:
            payload = self.api_client.fetch_transactions()

        except ConnectionError as error:
            raise BankApiError("Could not fetch bank transactions") from error

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
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def synchronize(
        self,
        importer: TransactionImporter,
    ) -> list[Transaction]:
        self.logger.info("Synchronizing %s", importer.source_name())

        if importer.supports_incremental_sync():
            self.logger.info("Running incremental sync")
        else:
            self.logger.info("Running full sync")

        transactions = importer.import_transactions()

        self.logger.info("Imported %s transactions", len(transactions))
        print()

        return transactions


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
    ]

    synchronizer = TransactionSynchronizer(
        logger=create_logger(),
    )

    for importer in importers:
        try:
            transactions = synchronizer.synchronize(importer)
        except TransactionImportError as error:
            synchronizer.logger.error(
                "Skipping importer %s: %s",
                importer.source_name(),
                error,
            )
            continue

        for transaction in transactions:
            print(transaction)


if __name__ == "__main__":
    main()
