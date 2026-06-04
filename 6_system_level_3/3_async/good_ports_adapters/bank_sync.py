import asyncio
from datetime import date
from decimal import Decimal

from .domain.models import Transaction
from .domain.use_cases import create_transaction
from .transaction_db_adapter import SyncDBTransactionRepository


class BankApiClient:
    async def fetch_transactions(self) -> list[Transaction]:
        await asyncio.sleep(0.25)  # Simulate network I/O

        return [
            Transaction(
                id="bank-tx-001",
                description="Coffee",
                category="Food",
                amount=Decimal("3.50"),
                currency="EUR",
                transaction_date=date(2026, 5, 1),
            ),
            Transaction(
                id="bank-tx-002",
                description="Train ticket",
                category="Transport",
                amount=Decimal("8.75"),
                currency="EUR",
                transaction_date=date(2026, 5, 4),
            ),
        ]


async def sync_bank_transactions(
    bank_client: BankApiClient,
    repository: SyncDBTransactionRepository,
) -> None:
    transactions = await bank_client.fetch_transactions()

    for transaction in transactions:
        create_transaction(transaction, repository)
