from datetime import date
from decimal import Decimal

from .models import Transaction


def load_transactions() -> list[Transaction]:
    return [
        Transaction(
            id="tx-001",
            description="Coffee",
            category="Food",
            amount=Decimal("3.50"),
            currency="EUR",
            transaction_date=date(2026, 5, 1),
        ),
        Transaction(
            id="tx-002",
            description="Groceries",
            category="Food",
            amount=Decimal("42.10"),
            currency="EUR",
            transaction_date=date(2026, 5, 3),
        ),
        Transaction(
            id="tx-003",
            description="Train ticket",
            category="Transport",
            amount=Decimal("8.75"),
            currency="EUR",
            transaction_date=date(2026, 5, 4),
        ),
        Transaction(
            id="tx-004",
            description="Book",
            category="Education",
            amount=Decimal("19.99"),
            currency="EUR",
            transaction_date=date(2026, 5, 6),
        ),
        Transaction(
            id="tx-005",
            description="Restaurant",
            category="Food",
            amount=Decimal("36.40"),
            currency="EUR",
            transaction_date=date(2026, 4, 28),
        ),
    ]
