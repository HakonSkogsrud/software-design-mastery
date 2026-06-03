from .domain.models import Transaction


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def list_all(self) -> list[Transaction]:
        return list(self._transactions)
