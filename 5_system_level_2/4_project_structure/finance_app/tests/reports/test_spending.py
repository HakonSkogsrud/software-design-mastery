from datetime import date
from decimal import Decimal

from reports.spending import generate_spending_report
from transactions.models import Transaction


def test_generate_spending_report_groups_totals_by_category() -> None:
    transactions = [
        Transaction("tx-001", "Coffee", "Food", Decimal("3.50"), "EUR", date(2026, 5, 1)),
        Transaction("tx-002", "Groceries", "Food", Decimal("42.10"), "EUR", date(2026, 5, 3)),
        Transaction("tx-003", "Train ticket", "Transport", Decimal("8.75"), "EUR", date(2026, 5, 4)),
    ]

    report = generate_spending_report(transactions)

    assert report.total_spent == Decimal("54.35")
    assert report.transaction_count == 3
    assert report.totals_by_category == {
        "Food": Decimal("45.60"),
        "Transport": Decimal("8.75"),
    }
