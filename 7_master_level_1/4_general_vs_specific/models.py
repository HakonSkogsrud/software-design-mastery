from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True)
class Transaction:
    description: str
    amount: Decimal
    transaction_type: TransactionType
    booked_at: date


@dataclass(frozen=True)
class MonthlySummary:
    month: int
    year: int
    total_income: Decimal
    total_expenses: Decimal

    @property
    def net_result(self) -> Decimal:
        return self.total_income - self.total_expenses
