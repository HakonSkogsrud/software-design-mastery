import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any


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

    def import_transactions(self) -> list[Transaction]:
        print(f"Loading transactions from {self.source_name()}")

        rows = self.read_rows()

        return self.parse_transactions(rows)

    def supports_incremental_sync(self) -> bool:
        return False

    def parse_transactions(
        self,
        rows: list[RawTransaction],
    ) -> list[Transaction]:
        return [self.parse_row(row) for row in rows]

    @abstractmethod
    def read_rows(self) -> list[RawTransaction]:
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

    def read_rows(self) -> list[RawTransaction]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return list(reader)

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

    def read_rows(self) -> list[RawTransaction]:
        with open(self.file_path) as json_file:
            data = json.load(json_file)

        return data["transactions"]

    def parse_row(self, row: RawTransaction) -> Transaction:
        return Transaction(
            id=str(row["transaction_id"]),
            description=str(row["merchant"]),
            category=str(row["category_name"]),
            amount=Decimal(str(row["amount_eur"])),
            currency="EUR",
            transaction_date=date.fromisoformat(str(row["booked_on"])),
        )


def synchronize_importer(
    importer: FileTransactionImporter,
) -> list[Transaction]:
    print(f"Synchronizing {importer.source_name()}")

    if importer.supports_incremental_sync():
        print("Running incremental sync")
    else:
        print("Running full sync")

    transactions = importer.import_transactions()

    print(f"Imported {len(transactions)} transactions")

    for transaction in transactions:
        print(transaction)

    print()

    return transactions


def main() -> None:
    importers: list[FileTransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BudgetingAppJsonImporter("budgeting_app_transactions.json"),
    ]

    for importer in importers:
        synchronize_importer(importer)


if __name__ == "__main__":
    main()
