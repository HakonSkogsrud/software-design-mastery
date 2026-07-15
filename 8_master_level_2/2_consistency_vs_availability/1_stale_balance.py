from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __str__(self) -> str:
        return f"€{self.amount:.2f}"


class AccountRepository:
    def __init__(self) -> None:
        self._balances: dict[str, Money] = {"account-123": Money(Decimal("1000.00"))}

    def get_balance(self, account_id: str) -> Money:
        print("Reading balance from the database")
        return self._balances[account_id]

    def record_payment(self, account_id: str, amount: Money) -> None:
        current = self._balances[account_id]
        self._balances[account_id] = Money(current.amount - amount.amount)


class BalanceCache:
    def __init__(self) -> None:
        self._balances: dict[str, Money] = {}

    def get(self, account_id: str) -> Money | None:
        return self._balances.get(account_id)

    def set(self, account_id: str, balance: Money) -> None:
        self._balances[account_id] = balance


def get_display_balance(
    account_id: str,
    repository: AccountRepository,
    cache: BalanceCache,
) -> Money:
    cached_balance = cache.get(account_id)

    if cached_balance is not None:
        print("Reading balance from the cache")
        return cached_balance

    balance = repository.get_balance(account_id)
    cache.set(account_id, balance)
    return balance


def main() -> None:
    repository = AccountRepository()
    cache = BalanceCache()
    account_id = "account-123"

    first_balance = get_display_balance(account_id, repository, cache)
    print(f"Displayed balance: {first_balance}")

    print("\nProcessing a payment of €250.00")
    repository.record_payment(account_id, Money(Decimal("250.00")))

    second_balance = get_display_balance(account_id, repository, cache)
    actual_balance = repository.get_balance(account_id)

    print(f"\nDisplayed balance: {second_balance}")
    print(f"Actual balance:    {actual_balance}")


if __name__ == "__main__":
    main()
