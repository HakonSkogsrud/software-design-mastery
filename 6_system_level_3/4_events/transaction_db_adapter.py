import asyncio

from domain.models import Transaction


class DatabaseTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    async def add(self, transaction: Transaction) -> None:
        await asyncio.sleep(0.01)  # Simulate database I/O
        self._transactions.append(transaction)

    async def list_all(self) -> list[Transaction]:
        await asyncio.sleep(0.01)  # Simulate database I/O
        return list(self._transactions)


class SyncDBTransactionRepository:
    def __init__(self, async_repository: DatabaseTransactionRepository) -> None:
        self._async_repository = async_repository

    def add(self, transaction: Transaction) -> None:
        asyncio.run(self._async_repository.add(transaction))

    def list_all(self) -> list[Transaction]:
        return asyncio.run(self._async_repository.list_all())
