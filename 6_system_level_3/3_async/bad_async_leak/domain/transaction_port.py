from typing import Protocol

from .models import Transaction


class TransactionRepository(Protocol):
    async def add(self, transaction: Transaction) -> None: ...

    async def list_all(self) -> list[Transaction]: ...
