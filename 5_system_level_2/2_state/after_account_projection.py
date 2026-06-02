# after_account_projection.py

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


class TransactionStore:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add_many(self, transactions: list[Transaction]) -> None:
        self._transactions.extend(transactions)

    def all(self) -> list[Transaction]:
        return list(self._transactions)


class AccountProjection:
    def __init__(self) -> None:
        self._balance = Decimal("0.00")
        self._totals_by_category: dict[str, Decimal] = {}

    def apply(self, transaction: Transaction) -> None:
        self._balance += transaction.amount

        current_total = self._totals_by_category.get(
            transaction.category,
            Decimal("0.00"),
        )
        self._totals_by_category[transaction.category] = (
            current_total + transaction.amount
        )

    def rebuild(self, transactions: list[Transaction]) -> None:
        self._balance = Decimal("0.00")
        self._totals_by_category.clear()

        for transaction in transactions:
            self.apply(transaction)

    def balance(self) -> Decimal:
        return self._balance

    def totals_by_category(self) -> dict[str, Decimal]:
        return dict(self._totals_by_category)


class CsvTransactionImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_transactions(self) -> list[Transaction]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            return [
                Transaction(
                    id=row["id"],
                    description=row["description"],
                    category=row["category"],
                    amount=Decimal(row["amount"]),
                    currency=row["currency"],
                    transaction_date=date.fromisoformat(row["transaction_date"]),
                )
                for row in reader
            ]

    def supports_incremental_sync(self) -> bool:
        return False

    def source_name(self) -> str:
        return "csv"


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
        payload = self.api_client.fetch_transactions()

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
    def __init__(
        self,
        store: TransactionStore,
        projection: AccountProjection,
        logger: Logger,
    ) -> None:
        self.store = store
        self.projection = projection
        self.logger = logger

    def synchronize(
        self,
        importer: TransactionImporter,
    ) -> None:
        self.logger.info("Synchronizing %s", importer.source_name())

        if importer.supports_incremental_sync():
            self.logger.info("Running incremental sync")
        else:
            self.logger.info("Running full sync")

        transactions = importer.import_transactions()

        self.store.add_many(transactions)

        for transaction in transactions:
            self.projection.apply(transaction)

        self.logger.info("Imported %s transactions", len(transactions))
        print()


def print_projection(projection: AccountProjection) -> None:
    print("Account projection")
    print("------------------")
    print(f"Balance: €{projection.balance()}")
    print()

    for category, total in projection.totals_by_category().items():
        print(f"- {category}: €{total}")


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("finance")


def main() -> None:
    store = TransactionStore()
    projection = AccountProjection()

    importers: list[TransactionImporter] = [
        CsvTransactionImporter("transactions.csv"),
        BankApiImporter(BankApiClient()),
    ]

    synchronizer = TransactionSynchronizer(
        store=store,
        projection=projection,
        logger=create_logger(),
    )

    for importer in importers:
        synchronizer.synchronize(importer)

    print_projection(projection)

    # Demonstrates that the projection is derived and rebuildable.
    projection.rebuild(store.all())


if __name__ == "__main__":
    main()
