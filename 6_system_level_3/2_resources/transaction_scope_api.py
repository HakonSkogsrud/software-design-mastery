# transaction_scope_api.py

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Protocol

from fastapi import FastAPI

app = FastAPI()


# -----------------------------
# Domain model
# -----------------------------


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


# -----------------------------
# Database connection
# -----------------------------


class DatabaseConnection:
    def connect(self) -> None:
        print("Opening database connection")

    def close(self) -> None:
        print("Closing database connection")

    def begin_transaction(self) -> None:
        print("Beginning database transaction")

    def commit(self) -> None:
        print("Committing database transaction")

    def rollback(self) -> None:
        print("Rolling back database transaction")

    def insert_transaction(self, transaction: Transaction) -> None:
        print(f"Saving transaction {transaction.id}")


@contextmanager
def transaction_scope() -> Iterator[DatabaseConnection]:
    connection = DatabaseConnection()

    connection.connect()
    connection.begin_transaction()

    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


# -----------------------------
# Port
# -----------------------------


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...


# -----------------------------
# Adapter
# -----------------------------


class SqlTransactionRepository:
    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    def add(self, transaction: Transaction) -> None:
        self._connection.insert_transaction(transaction)


# -----------------------------
# Application logic
# -----------------------------


def create_transaction(
    transaction: Transaction,
    repository: TransactionRepository,
) -> None:
    repository.add(transaction)


def update_monthly_budget(
    category: str,
    amount: Decimal,
) -> None:
    print(f"Updating budget for {category}: {amount}")


# -----------------------------
# REST API
# -----------------------------


@app.post("/transactions")
def create_transaction_endpoint(
    request: dict[str, Any],
) -> dict[str, str]:
    with transaction_scope() as connection:
        repository = SqlTransactionRepository(connection)

        transaction = Transaction(
            id=request["id"],
            description=request["description"],
            category=request["category"],
            amount=Decimal(request["amount"]),
            currency=request["currency"],
            transaction_date=date.fromisoformat(request["transaction_date"]),
        )

        create_transaction(transaction, repository)

        update_monthly_budget(
            category=transaction.category,
            amount=transaction.amount,
        )

        return {"status": "created"}
