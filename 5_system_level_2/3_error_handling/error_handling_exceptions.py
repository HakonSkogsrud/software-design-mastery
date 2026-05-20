# error_handling_exceptions.py

import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable, Protocol


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
    def import_transactions(self) -> Iterable[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


class SpendingSummary:
    def __init__(self) -> None:
        self._totals_by_category: dict[str, Decimal] = {}

    def record(self, transaction: Transaction) -> None:
        current_total = self._totals_by_category.get(
            transaction.category,
            Decimal("0.00"),
        )

        self._totals_by_category[transaction.category] = (
            current_total + transaction.amount
        )

    def totals_by_category(self) -> dict[str, Decimal]:
        return dict(self._totals_by_category)


class CsvTransactionImporter:
    def __init__(self, file_path: str, logger: Logger) -> None:
        self.file_path = file_path
        self.logger = logger

    def import_transactions(self) -> Iterable[Transaction]:
        self.logger.info("Streaming transactions from %s", self.file_path)

        try:
            csv_file = open(self.file_path, newline="")
        except OSError as error:
            raise TransactionImportError(
                f"Could not open transaction file: {self.file_path}"
            ) from error

        with csv_file:
            reader = csv.DictReader(csv_file)

            for line_number, row in enumerate(reader, start=2):
                yield self._parse_transaction(row, line_number)

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
    def __init__(self, logger: Logger, should_fail: bool = False) -> None:
        self.logger = logger
        self.should_fail = should_fail

    def fetch_transactions(self) -> list[dict[str, str]]:
        self.logger.info("Calling bank API")

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
    def __init__(self, api_client: BankApiClient, logger: Logger) -> None:
        self.api_client = api_client
        self.logger = logger

    def import_transactions(self) -> Iterable[Transaction]:
        self.logger.info("Fetching transactions from bank API")

        try:
            payload = self.api_client.fetch_transactions()
        except ConnectionError as error:
            raise BankApiError("Could not fetch bank transactions") from error

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
    summary: SpendingSummary,
    logger: Logger,
) -> None:
    logger.info("Synchronizing %s", importer.source_name())

    if importer.supports_incremental_sync():
        logger.info("Running incremental sync")
    else:
        logger.info("Running full sync")

    transactions = importer.import_transactions()
    transactions = filter_by_currency(transactions, "EUR", logger)

    transaction_count = 0

    for transaction in transactions:
        print(transaction)
        summary.record(transaction)
        transaction_count += 1

    logger.info("Imported %s transactions", transaction_count)
    print()


def print_spending_summary(summary: SpendingSummary) -> None:
    print("Spending summary")
    print("----------------")

    for category, total in summary.totals_by_category().items():
        print(f"- {category}: €{total}")


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    logger = create_logger()
    summary = SpendingSummary()

    api_client = BankApiClient(logger)

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv", logger),
        BankApiImporter(api_client, logger),
    ]

    for importer in importers:
        try:
            synchronize_importer(importer, summary, logger)
        except TransactionImportError as error:
            logger.error(
                "Skipping importer %s: %s",
                importer.source_name(),
                error,
            )

    print_spending_summary(summary)


if __name__ == "__main__":
    main()
