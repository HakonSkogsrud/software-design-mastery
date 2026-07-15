from dataclasses import dataclass
from decimal import Decimal
from threading import Lock, Thread
from time import sleep


class InsufficientFundsError(Exception):
    pass


@dataclass
class Account:
    id: str
    balance: Decimal


class UnsafeAccountRepository:
    def __init__(self) -> None:
        self._account = Account(
            id="account-123",
            balance=Decimal("100.00"),
        )

    def get_balance(self, account_id: str) -> Decimal:
        return self._account.balance

    def save_balance(
        self,
        account_id: str,
        new_balance: Decimal,
    ) -> None:
        self._account.balance = new_balance


def unsafe_withdraw(
    repository: UnsafeAccountRepository,
    account_id: str,
    amount: Decimal,
) -> None:
    balance = repository.get_balance(account_id)

    if balance < amount:
        raise InsufficientFundsError()

    # Simulate work happening between reading and writing.
    sleep(0.1)

    repository.save_balance(
        account_id,
        balance - amount,
    )

    print(f"Approved withdrawal of €{amount:.2f}")


class SafeAccountRepository:
    def __init__(self) -> None:
        self._account = Account(
            id="account-123",
            balance=Decimal("100.00"),
        )
        self._lock = Lock()

    def withdraw_if_funds_available(
        self,
        account_id: str,
        amount: Decimal,
    ) -> None:
        with self._lock:
            if self._account.balance < amount:
                raise InsufficientFundsError()

            sleep(0.1)
            self._account.balance -= amount

    def get_balance(self, account_id: str) -> Decimal:
        return self._account.balance


def safe_withdraw(
    repository: SafeAccountRepository,
    account_id: str,
    amount: Decimal,
) -> None:
    try:
        repository.withdraw_if_funds_available(
            account_id,
            amount,
        )
        print(f"Approved withdrawal of €{amount:.2f}")
    except InsufficientFundsError:
        print(f"Rejected withdrawal of €{amount:.2f}")


def run_unsafe_example() -> None:
    print("UNSAFE VERSION")

    repository = UnsafeAccountRepository()
    account_id = "account-123"

    threads = [
        Thread(
            target=unsafe_withdraw,
            args=(repository, account_id, Decimal("80.00")),
        )
        for _ in range(2)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Final stored balance: €{repository.get_balance(account_id):.2f}")


def run_safe_example() -> None:
    print("\nSAFE VERSION")

    repository = SafeAccountRepository()
    account_id = "account-123"

    threads = [
        Thread(
            target=safe_withdraw,
            args=(repository, account_id, Decimal("80.00")),
        )
        for _ in range(2)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Final stored balance: €{repository.get_balance(account_id):.2f}")


def main() -> None:
    run_unsafe_example()
    run_safe_example()


if __name__ == "__main__":
    main()
