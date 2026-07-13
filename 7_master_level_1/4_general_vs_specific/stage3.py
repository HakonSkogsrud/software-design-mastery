from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from models import MonthlySummary, Transaction, TransactionType


@dataclass(frozen=True)
class TransactionTotals:
    income: Decimal
    expenses: Decimal

    @property
    def net(self) -> Decimal:
        return self.income - self.expenses


def transactions_in_period(
    transactions: list[Transaction],
    *,
    start: date,
    end: date,
) -> list[Transaction]:
    return [
        transaction
        for transaction in transactions
        if start <= transaction.booked_at <= end
    ]


def calculate_transaction_totals(
    transactions: list[Transaction],
) -> TransactionTotals:
    income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == TransactionType.INCOME
    )

    expenses = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == TransactionType.EXPENSE
    )

    return TransactionTotals(
        income=income,
        expenses=expenses,
    )


def generate_monthly_summary(
    transactions: list[Transaction],
    *,
    month: int,
    year: int,
) -> MonthlySummary:
    monthly_transactions = transactions_in_period(
        transactions,
        start=date(year, month, 1),
        end=date(year, month, 30),
    )

    totals = calculate_transaction_totals(monthly_transactions)

    return MonthlySummary(
        month=month,
        year=year,
        total_income=totals.income,
        total_expenses=totals.expenses,
    )


def generate_tax_summary(
    transactions: list[Transaction],
) -> None:
    print("Tax summary")


def generate_cashflow_summary(
    transactions: list[Transaction],
) -> None:
    print("Cashflow summary")
