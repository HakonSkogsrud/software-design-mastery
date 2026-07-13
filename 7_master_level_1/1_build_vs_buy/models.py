from decimal import Decimal

from pydantic import BaseModel


class TransactionInput(BaseModel):
    account_id: str
    amount: Decimal
    currency: str
    description: str = ""
