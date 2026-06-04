from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Annotated, Any, Iterator, Protocol

from fastapi import Depends, FastAPI

app = FastAPI()


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    category: str
    amount: Decimal
    currency: str
    transaction_date: date


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...


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


class SqlTransactionRepository:
    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    def add(self, transaction: Transaction) -> None:
        self._connection.insert_transaction(transaction)


def get_transaction_connection() -> Iterator[DatabaseConnection]:
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


def get_transaction_repository(
    connection: Annotated[
        DatabaseConnection,
        Depends(get_transaction_connection),
    ],
) -> TransactionRepository:
    return SqlTransactionRepository(connection)


def create_transaction(
    transaction: Transaction,
    repository: TransactionRepository,
) -> None:
    repository.add(transaction)


def update_monthly_budget(category: str, amount: Decimal) -> None:
    print(f"Updating budget for {category}: {amount}")


@app.post("/transactions")
def create_transaction_endpoint(
    request: dict[str, Any],
    repository: Annotated[
        TransactionRepository,
        Depends(get_transaction_repository),
    ],
) -> dict[str, str]:
    transaction = Transaction(
        id=request["id"],
        description=request["description"],
        category=request["category"],
        amount=Decimal(request["amount"]),
        currency=request["currency"],
        transaction_date=date.fromisoformat(request["transaction_date"]),
    )

    create_transaction(transaction, repository)
    update_monthly_budget(transaction.category, transaction.amount)

    return {"status": "created"}
