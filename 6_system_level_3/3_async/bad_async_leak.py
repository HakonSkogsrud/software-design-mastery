from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any
import asyncio

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
# Infrastructure detail leaks inward
# -----------------------------


class AsyncDatabaseTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    async def add(self, transaction: Transaction) -> None:
        await asyncio.sleep(0.01)  # Simulate database I/O
        self._transactions.append(transaction)

    async def list_all(self) -> list[Transaction]:
        await asyncio.sleep(0.01)  # Simulate database I/O
        return list(self._transactions)


# -----------------------------
# Application logic now depends on async infrastructure
# -----------------------------


async def create_transaction(
    transaction: Transaction,
    repository: AsyncDatabaseTransactionRepository,
) -> None:
    await repository.add(transaction)


async def calculate_total_spending(transactions: list[Transaction]) -> Decimal:
    # This function has no I/O, but async has leaked into it anyway.
    total = Decimal("0.00")

    for transaction in transactions:
        total += transaction.amount

    return total


async def calculate_spending_by_category(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    # Also no I/O. This should not need to be async.
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        totals.setdefault(transaction.category, Decimal("0.00"))
        totals[transaction.category] += transaction.amount

    return totals


async def filter_transactions_by_month(
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


async def generate_spending_report(
    transactions: list[Transaction],
) -> SpendingReport:
    return SpendingReport(
        total_spent=await calculate_total_spending(transactions),
        totals_by_category=await calculate_spending_by_category(transactions),
        transaction_count=len(transactions),
    )


async def generate_monthly_spending_report(
    repository: AsyncDatabaseTransactionRepository,
    year: int,
    month: int,
) -> SpendingReport:
    transactions = await repository.list_all()
    monthly_transactions = await filter_transactions_by_month(
        transactions,
        year=year,
        month=month,
    )
    return await generate_spending_report(monthly_transactions)


# -----------------------------
# REST API adapter
# -----------------------------


repository = AsyncDatabaseTransactionRepository()


@app.post("/transactions")
async def create_transaction_endpoint(request: dict[str, Any]) -> dict[str, str]:
    transaction = Transaction(
        id=request["id"],
        description=request["description"],
        category=request["category"],
        amount=Decimal(request["amount"]),
        currency=request["currency"],
        transaction_date=date.fromisoformat(request["transaction_date"]),
    )

    await create_transaction(transaction, repository)

    return {"status": "created"}


@app.get("/summary")
async def get_summary_endpoint(year: int, month: int) -> dict[str, Any]:
    report = await generate_monthly_spending_report(
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
# CLI entry point now also needs async plumbing
# -----------------------------


async def run_cli_report() -> None:
    repository = AsyncDatabaseTransactionRepository()

    await create_transaction(
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

    await create_transaction(
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

    report = await generate_monthly_spending_report(repository, year=2026, month=5)

    print("Spending report")
    print("---------------")
    print(f"Total spent: EUR {report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    for category, total in report.totals_by_category.items():
        print(f"- {category}: EUR {total}")


if __name__ == "__main__":
    asyncio.run(run_cli_report())
