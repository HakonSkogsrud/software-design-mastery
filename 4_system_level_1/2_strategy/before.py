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


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int


def generate_spending_report(
    transactions: list[Transaction],
    report_type: str,
    minimum_amount: Decimal | None = None,
    category: str | None = None,
) -> SpendingReport:
    filtered_transactions: list[Transaction] = []

    for transaction in transactions:
        if report_type == "all":
            filtered_transactions.append(transaction)

        elif report_type == "exclude_refunds":
            if transaction.amount >= 0:
                filtered_transactions.append(transaction)

        elif report_type == "large_purchases":
            if transaction.amount >= Decimal("100.00"):
                filtered_transactions.append(transaction)

        elif report_type == "minimum_amount":
            if minimum_amount is not None and transaction.amount >= minimum_amount:
                filtered_transactions.append(transaction)

        elif report_type == "category":
            if category is not None and transaction.category == category:
                filtered_transactions.append(transaction)

        else:
            raise ValueError(f"Unknown report type: {report_type}")

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
        report_type="large_purchases",
    )

    print_report(report)


if __name__ == "__main__":
    main()
