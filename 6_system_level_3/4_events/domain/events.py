from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from .models import Transaction


@dataclass(frozen=True)
class TransactionCreated:
    transaction_id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date
    occurred_at: datetime

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> "TransactionCreated":
        return cls(
            transaction_id=transaction.id,
            description=transaction.description,
            category=transaction.category,
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_date=transaction.transaction_date,
            occurred_at=datetime.now(),
        )
