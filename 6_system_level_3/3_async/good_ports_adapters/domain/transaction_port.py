from typing import Protocol

from .models import Transaction


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...

    def list_all(self) -> list[Transaction]: ...
