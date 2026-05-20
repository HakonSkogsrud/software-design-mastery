# after_ports_and_adapters.py

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Protocol

from fastapi import FastAPI

app = FastAPI()


# -----------------------------
# Domain model
# -----------------------------


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


# -----------------------------
# Port
# -----------------------------


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...

    def list_all(self) -> list[Transaction]: ...


# -----------------------------
# Application logic
# -----------------------------


def create_transaction(
    transaction: Transaction,
    repository: TransactionRepository,
) -> None:
    repository.add(transaction)


def calculate_total_spending(transactions: list[Transaction]) -> Decimal:
    total = Decimal("0.00")

    for transaction in transactions:
        total += transaction.amount

    return total


def calculate_spending_by_category(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        totals.setdefault(transaction.category, Decimal("0.00"))
        totals[transaction.category] += transaction.amount

    return totals


def filter_transactions_by_month(
    transactions: list[Transaction],
    year: int,
    month: int,
) -> list[Transaction]:
    return [
        transaction
        for transaction in transactions
        if transaction.transaction_date.year == year
        and transaction.transaction_date.month == month
    ]


def generate_spending_report(
    transactions: list[Transaction],
) -> SpendingReport:
    return SpendingReport(
        total_spent=calculate_total_spending(transactions),
        totals_by_category=calculate_spending_by_category(transactions),
        transaction_count=len(transactions),
    )


def generate_monthly_spending_report(
    repository: TransactionRepository,
    year: int,
    month: int,
) -> SpendingReport:
    transactions = repository.list_all()

    monthly_transactions = filter_transactions_by_month(
        transactions,
        year=year,
        month=month,
    )

    return generate_spending_report(monthly_transactions)


# -----------------------------
# Adapter: in-memory storage
# -----------------------------


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def list_all(self) -> list[Transaction]:
        return list(self._transactions)


# -----------------------------
# Adapter: REST API
# -----------------------------

repository = InMemoryTransactionRepository()


@app.post("/transactions")
def create_transaction_endpoint(request: dict[str, Any]) -> dict[str, str]:
    transaction = Transaction(
        id=request["id"],
        description=request["description"],
        category=request["category"],
        amount=Decimal(request["amount"]),
        currency=request["currency"],
        transaction_date=date.fromisoformat(request["transaction_date"]),
    )

    create_transaction(transaction, repository)

    return {"status": "created"}


@app.get("/summary")
def get_summary_endpoint(year: int, month: int) -> dict[str, Any]:
    report = generate_monthly_spending_report(
        repository,
        year=year,
        month=month,
    )

    return {
        "total_spent": str(report.total_spent),
        "transaction_count": report.transaction_count,
        "totals_by_category": {
            category: str(total)
            for category, total in report.totals_by_category.items()
        },
    }


# -----------------------------
# Adapter: CLI-style entry point
# -----------------------------


def print_report(report: SpendingReport) -> None:
    print("Spending report")
    print("---------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")


def run_cli_report() -> None:
    repository = InMemoryTransactionRepository()

    create_transaction(
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("3.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        repository,
    )

    create_transaction(
        Transaction(
            id="tx-002",
            description="Train ticket",
            category="Transport",
            amount=Decimal("8.75"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
        repository,
    )

    report = generate_monthly_spending_report(
        repository,
        year=2026,
        month=5,
    )

    print_report(report)


if __name__ == "__main__":
    run_cli_report()
