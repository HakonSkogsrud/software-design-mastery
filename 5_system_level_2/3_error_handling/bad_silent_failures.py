import csv
import logging
from dataclasses import dataclass
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
        transactions: list[Transaction] = []

        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try:
                    transactions.append(
                        Transaction(
                            id=row["id"],
                            description=row["description"],
                            category=row["category"],
                            amount=Decimal(row["amount"]),
                            currency=row["currency"],
                            transaction_date=date.fromisoformat(
                                row["transaction_date"]
                            ),
                        )
                    )
                except Exception:
                    # Bad: broken rows disappear silently.
                    pass

        return transactions

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"


class TransactionSynchronizer:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def synchronize(
        self,
        importer: TransactionImporter,
    ) -> list[Transaction]:
        self.logger.info("Synchronizing %s", importer.source_name())

        transactions = importer.import_transactions()

        self.logger.info("Imported %s transactions", len(transactions))
        print()

        return transactions


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    importer = CsvTransactionImporter("transactions_with_errors.csv")

    synchronizer = TransactionSynchronizer(
        logger=create_logger(),
    )

    transactions = synchronizer.synchronize(importer)

    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    main()
