from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class TransactionInput:
    account_id: str
    amount: Decimal
    currency: str
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TransactionInput":
        required_fields = ("account_id", "amount", "currency")

        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required")

        return cls(
            account_id=str(data["account_id"]),
            amount=Decimal(str(data["amount"])),
            currency=str(data["currency"]),
            description=str(data.get("description", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "amount": str(self.amount),
            "currency": self.currency,
            "description": self.description,
        }
