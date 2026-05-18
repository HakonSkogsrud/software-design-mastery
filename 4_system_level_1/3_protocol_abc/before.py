import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


class CsvTransactionImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> list[Transaction]:
        print(f"Loading transactions from {self.file_path}")

        rows = self._read_rows()

        return self._parse_transactions(rows)

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"

    def _read_rows(self) -> list[dict[str, str]]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            return list(reader)

    def _parse_transactions(
        self,
        rows: list[dict[str, str]],
    ) -> list[Transaction]:
        return [
            Transaction(
                id=row["id"],
                description=row["description"],
                category=row["category"],
                amount=Decimal(row["amount"]),
                currency=row["currency"],
                transaction_date=date.fromisoformat(row["transaction_date"]),
            )
            for row in rows
        ]


def synchronize_importer(importer: CsvTransactionImporter) -> None:
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


def main() -> None:
    importer = CsvTransactionImporter("transactions.csv")

    synchronize_importer(importer)


if __name__ == "__main__":
    main()
