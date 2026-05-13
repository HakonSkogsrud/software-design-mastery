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


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int


class TransactionFilter(Protocol):
    def include(
        self,
        transaction: Transaction,
    ) -> bool: ...


def generate_spending_report(
    transactions: list[Transaction],
    transaction_filter: TransactionFilter,
) -> SpendingReport:
    filtered_transactions = [
        transaction
        for transaction in transactions
        if transaction_filter.include(transaction)
    ]

    total_spent = sum(
        (transaction.amount for transaction in filtered_transactions), Decimal("0")
    )

    totals_by_category: dict[str, Decimal] = {}

    for transaction in filtered_transactions:
        if transaction.category not in totals_by_category:
            totals_by_category[transaction.category] = Decimal("0.00")

        totals_by_category[transaction.category] += transaction.amount

    return SpendingReport(
        total_spent=total_spent,
        totals_by_category=totals_by_category,
        transaction_count=len(filtered_transactions),
    )


def print_report(report: SpendingReport) -> None:
    print("Spending Report")
    print("----------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    print("By category:")
    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")


class ExcludeRefunds:
    def include(
        self,
        transaction: Transaction,
    ) -> bool:
        return transaction.amount >= 0


class LargePurchasesOnly:
    def __init__(
        self,
        minimum_amount: Decimal,
    ) -> None:
        self.minimum_amount = minimum_amount

    def include(
        self,
        transaction: Transaction,
    ) -> bool:
        return transaction.amount >= self.minimum_amount


class CategoryOnly:
    def __init__(
        self,
        category: str,
    ) -> None:
        self.category = category

    def include(
        self,
        transaction: Transaction,
    ) -> bool:
        return transaction.category == self.category


def load_transactions() -> list[Transaction]:
    return [
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("4.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        Transaction(
            id="tx-002",
            description="Salary refund",
            category="Income",
            amount=Decimal("-200.00"),
            currency="EUR",
            transaction_date=date(2026, 5, 2),
        ),
        Transaction(
            id="tx-003",
            description="Laptop",
            category="Electronics",
            amount=Decimal("1200.00"),
            currency="EUR",
            transaction_date=date(2026, 5, 3),
        ),
        Transaction(
            id="tx-004",
            description="Groceries",
            category="Food",
            amount=Decimal("58.20"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
    ]


def main() -> None:
    transactions = load_transactions()

    report = generate_spending_report(
        transactions,
        transaction_filter=LargePurchasesOnly(minimum_amount=Decimal("100.00")),
    )

    print_report(report)

    print()
    print("Food-only report")
    print("================")

    food_report = generate_spending_report(
        transactions,
        transaction_filter=CategoryOnly("Food"),
    )

    print_report(food_report)


if __name__ == "__main__":
    main()
