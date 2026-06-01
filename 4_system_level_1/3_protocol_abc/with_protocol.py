import csv
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


class TransactionImporter(Protocol):
    def import_transactions(self) -> list[Transaction]: ...

    def supports_incremental_sync(self) -> bool: ...

    def source_name(self) -> str: ...


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
        print("Fetching transactions from bank API")

        payload = self.api_client.fetch_transactions()

        return self._normalize(payload)

    def supports_incremental_sync(self) -> bool:
        return True

    def source_name(self) -> str:
        return "bank_api"

    def _normalize(
        self,
        payload: list[dict[str, str]],
    ) -> list[Transaction]:
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


class FakeImporter:
    def import_transactions(self) -> list[Transaction]:
        return [
            Transaction(
                id="test-001",
                description="Test transaction",
                category="Testing",
                amount=Decimal("10.00"),
                currency="EUR",
                transaction_date=date(2026, 5, 10),
            )
        ]

    def supports_incremental_sync(self) -> bool:
        return True

    def source_name(self) -> str:
        return "fake"


def synchronize_importer(
    importer: TransactionImporter,
) -> list[Transaction]:
    print(f"Synchronizing {importer.source_name()}")

    if importer.supports_incremental_sync():
        print("Running incremental sync")
    else:
        print("Running full sync")

    transactions = importer.import_transactions()

    print(f"Imported {len(transactions)} transactions")

    return transactions


def main() -> None:
    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
        FakeImporter(),
    ]

    for importer in importers:
        synchronize_importer(importer)


if __name__ == "__main__":
    main()
