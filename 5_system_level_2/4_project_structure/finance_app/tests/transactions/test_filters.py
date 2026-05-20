from datetime import date
from decimal import Decimal

from transactions.filters import filter_transactions_by_month
from transactions.models import Transaction


def test_filter_transactions_by_month_returns_only_matching_month() -> None:
    transactions = [
        Transaction("tx-001", "Coffee", "Food", Decimal("3.50"), "EUR", date(2026, 5, 1)),
        Transaction("tx-002", "Restaurant", "Food", Decimal("36.40"), "EUR", date(2026, 4, 28)),
    ]

    result = filter_transactions_by_month(transactions, year=2026, month=5)

    assert [transaction.id for transaction in result] == ["tx-001"]
