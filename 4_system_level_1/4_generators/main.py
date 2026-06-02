import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Iterable


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


type RawTransaction = dict[str, Any]


class FileTransactionImporter(ABC):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> Iterable[Transaction]:
        print(f"Streaming transactions from {self.source_name()}")

        for row in self.read_rows():
            yield self.parse_row(row)

    def supports_incremental_sync(self) -> bool:
        return False

    @abstractmethod
    def read_rows(self) -> Iterable[RawTransaction]:
        pass

    @abstractmethod
    def parse_row(self, row: RawTransaction) -> Transaction:
        pass

    @abstractmethod
    def source_name(self) -> str:
        pass


class CsvTransactionImporter(FileTransactionImporter):
    def source_name(self) -> str:
        return "csv"

    def read_rows(self) -> Iterable[RawTransaction]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                yield row

    def parse_row(self, row: RawTransaction) -> Transaction:
        return Transaction(
            id=str(row["id"]),
            description=str(row["description"]),
            category=str(row["category"]),
            amount=Decimal(str(row["amount"])),
            currency=str(row["currency"]),
            transaction_date=date.fromisoformat(str(row["transaction_date"])),
        )


class BudgetingAppJsonImporter(FileTransactionImporter):
    def source_name(self) -> str:
        return "budgeting_app_json"

    def read_rows(self) -> Iterable[RawTransaction]:
        with open(self.file_path) as json_file:
            data = json.load(json_file)

        yield from data["transactions"]

    def parse_row(self, row: RawTransaction) -> Transaction:
        return Transaction(
            id=str(row["transaction_id"]),
            description=str(row["merchant"]),
            category=str(row["category_name"]),
            amount=Decimal(str(row["amount_eur"])),
            currency="EUR",
            transaction_date=date.fromisoformat(str(row["booked_on"])),
        )


def filter_by_category(
    transactions: Iterable[Transaction],
    category: str,
) -> Iterable[Transaction]:
    for transaction in transactions:
        if transaction.category == category:
            yield transaction


def synchronize_importer(
    importer: FileTransactionImporter,
) -> Iterable[Transaction]:
    print(f"Synchronizing {importer.source_name()}")

    if importer.supports_incremental_sync():
        print("Running incremental sync")
    else:
        print("Running full sync")

    transaction_count = 0

    for transaction in importer.import_transactions():
        transaction_count += 1
        print(transaction)
        yield transaction

    print(f"Imported {transaction_count} transactions")
    print()


def main() -> None:
    importers: list[FileTransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BudgetingAppJsonImporter("budgeting_app_transactions.json"),
    ]

    for importer in importers:
        transactions = synchronize_importer(importer)
        food_transactions = filter_by_category(transactions, "Food")

        for transaction in food_transactions:
            print(f"Selected transaction: {transaction.description}")


if __name__ == "__main__":
    main()
