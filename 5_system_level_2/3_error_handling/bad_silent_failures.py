# bad_silent_failures.py

import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


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
    def __init__(self, file_path: str, logger: logging.Logger) -> None:
        self.file_path = file_path
        self.logger = logger

    def import_transactions(self) -> Iterable[Transaction]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try:
                    yield Transaction(
                        id=row["id"],
                        description=row["description"],
                        category=row["category"],
                        amount=Decimal(row["amount"]),
                        currency=row["currency"],
                        transaction_date=date.fromisoformat(row["transaction_date"]),
                    )
                except Exception:
                    # Bad: the system silently ignores broken data.
                    pass


def print_spending_summary(summary: SpendingSummary) -> None:
    print("Spending summary")
    print("----------------")

    for category, total in summary.totals_by_category().items():
        print(f"- {category}: €{total}")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("finance")

    summary = SpendingSummary()
    importer = CsvTransactionImporter("transactions_with_errors.csv", logger)

    for transaction in importer.import_transactions():
        print(transaction)
        summary.record(transaction)

    print()
    print_spending_summary(summary)


if __name__ == "__main__":
    main()
