from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __mul__(self, factor: Decimal) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __gt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare amounts in different currencies")
        return self.amount > other.amount

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class Transaction:
    amount: Money


@dataclass(frozen=True)
class Exchange:
    amount: Money


EUR = "EUR"


def apply_high_value_discount(fee: Money, amount: Money) -> Money:
    if amount > Money(Decimal("10000"), EUR):
        return fee * Decimal("0.9")

    return fee


def calculate_transfer_fee(transaction: Transaction) -> Money:
    fee = transaction.amount * Decimal("0.015")
    return apply_high_value_discount(fee, transaction.amount)


def calculate_exchange_fee(exchange: Exchange) -> Money:
    fee = exchange.amount * Decimal("0.015")
    return apply_high_value_discount(fee, exchange.amount)


def main() -> None:
    transfer = Transaction(Money(Decimal("12000"), EUR))
    exchange = Exchange(Money(Decimal("8000"), EUR))

    print("Transfer fee:", calculate_transfer_fee(transfer))
    print("Exchange fee:", calculate_exchange_fee(exchange))


if __name__ == "__main__":
    main()
