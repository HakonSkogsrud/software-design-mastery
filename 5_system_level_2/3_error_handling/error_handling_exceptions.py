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
    def __init__(
        self,
        source: str,
        line_number: int,
        field: str,
        value: str,
    ) -> None:
        self.source = source
        self.line_number = line_number
        self.field = field
        self.value = value

        super().__init__(
            f"Invalid value '{value}' for field '{field}' "
            f"in {source} on line {line_number}"
        )


class MissingTransactionFieldError(TransactionImportError):
    def __init__(
        self,
        source: str,
        line_number: int,
        field: str,
    ) -> None:
        self.source = source
        self.line_number = line_number
        self.field = field

        super().__init__(f"Missing field '{field}' in {source} on line {line_number}")


class UnsupportedCurrencyError(TransactionImportError):
    def __init__(
        self,
        source: str,
        currency: str,
        transaction_id: str,
    ) -> None:
        self.source = source
        self.currency = currency
        self.transaction_id = transaction_id

        super().__init__(
            f"Unsupported currency '{currency}' "
            f"for transaction '{transaction_id}' from {source}"
        )


class BankApiError(TransactionImportError):
    def __init__(
        self,
        endpoint: str,
        reason: str,
    ) -> None:
        self.endpoint = endpoint
        self.reason = reason

        super().__init__(f"Bank API call to '{endpoint}' failed: {reason}")


SUPPORTED_CURRENCIES = {"EUR", "USD"}


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
        transaction_id = self._required(row, "id", line_number)
        description = self._required(row, "description", line_number)
        category = self._required(row, "category", line_number)
        amount_text = self._required(row, "amount", line_number)
        currency = self._required(row, "currency", line_number)
        transaction_date_text = self._required(
            row,
            "transaction_date",
            line_number,
        )

        try:
            amount = Decimal(amount_text)
        except InvalidOperation as error:
            raise InvalidTransactionError(
                source=self.file_path,
                line_number=line_number,
                field="amount",
                value=amount_text,
            ) from error

        try:
            transaction_date = date.fromisoformat(transaction_date_text)
        except ValueError as error:
            raise InvalidTransactionError(
                source=self.file_path,
                line_number=line_number,
                field="transaction_date",
                value=transaction_date_text,
            ) from error

        if currency not in SUPPORTED_CURRENCIES:
            raise UnsupportedCurrencyError(
                source=self.file_path,
                currency=currency,
                transaction_id=transaction_id,
            )

        if amount <= Decimal("0.00"):
            raise InvalidTransactionError(
                source=self.file_path,
                line_number=line_number,
                field="amount",
                value=amount_text,
            )

        return Transaction(
            id=transaction_id,
            description=description,
            category=category,
            amount=amount,
            currency=currency,
            transaction_date=transaction_date,
        )

    def _required(
        self,
        row: dict[str, str],
        field: str,
        line_number: int,
    ) -> str:
        try:
            value = row[field]
        except KeyError as error:
            raise MissingTransactionFieldError(
                source=self.file_path,
                line_number=line_number,
                field=field,
            ) from error

        if value == "":
            raise MissingTransactionFieldError(
                source=self.file_path,
                line_number=line_number,
                field=field,
            )

        return value

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
            raise BankApiError(
                endpoint="/transactions",
                reason=str(error),
            ) from error

        return [self._parse_transaction(item) for item in payload]

    def _parse_transaction(self, item: dict[str, str]) -> Transaction:
        transaction_id = item["transaction_id"]
        currency = item["currency_code"]

        if currency not in SUPPORTED_CURRENCIES:
            raise UnsupportedCurrencyError(
                source="bank_api",
                currency=currency,
                transaction_id=transaction_id,
            )

        return Transaction(
            id=transaction_id,
            description=item["details"],
            category=item["type"],
            amount=Decimal(item["value"]),
            currency=currency,
            transaction_date=date.fromisoformat(item["date_posted"]),
        )

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
    logger = create_logger()

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions_with_errors.csv"),
        BankApiImporter(BankApiClient()),
    ]

    synchronizer = TransactionSynchronizer(logger)

    for importer in importers:
        try:
            transactions = synchronizer.synchronize(importer)

        except InvalidTransactionError as error:
            logger.error(
                "Invalid transaction in %s on line %s: %s=%s",
                error.source,
                error.line_number,
                error.field,
                error.value,
            )
            continue

        except MissingTransactionFieldError as error:
            logger.error(
                "Missing field in %s on line %s: %s",
                error.source,
                error.line_number,
                error.field,
            )
            continue

        except UnsupportedCurrencyError as error:
            logger.error(
                "Unsupported currency in %s: transaction=%s currency=%s",
                error.source,
                error.transaction_id,
                error.currency,
            )
            continue

        except BankApiError as error:
            logger.error(
                "Bank API error at %s: %s",
                error.endpoint,
                error.reason,
            )
            continue

        except TransactionImportError as error:
            logger.error("Import failed: %s", error)
            continue

        for transaction in transactions:
            print(transaction)


if __name__ == "__main__":
    main()
