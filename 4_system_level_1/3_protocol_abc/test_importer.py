from datetime import date
from decimal import Decimal

from with_protocol import Transaction, synchronize_importer


class FakeImporter:
    def import_transactions(self) -> list[Transaction]:
        return [
            Transaction(
                id="test-001",
                description="Coffee",
                category="Food",
                amount=Decimal("3.50"),
                currency="EUR",
                transaction_date=date(2026, 5, 1),
            ),
            Transaction(
                id="test-002",
                description="Train ticket",
                category="Transport",
                amount=Decimal("8.75"),
                currency="EUR",
                transaction_date=date(2026, 5, 4),
            ),
        ]

    def supports_incremental_sync(self) -> bool:
        return True

    def source_name(self) -> str:
        return "fake"


def test_synchronize_importer_uses_any_compatible_importer() -> None:
    importer = FakeImporter()

    transactions = synchronize_importer(importer)

    assert len(transactions) == 2
    assert transactions[0].description == "Coffee"
    assert transactions[1].category == "Transport"
