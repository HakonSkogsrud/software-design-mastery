from fastapi import FastAPI
from models import TransactionInput
from policies import SupportedCurrencyPolicy
from services import TransactionService

app = FastAPI()

currency_policy = SupportedCurrencyPolicy({"EUR", "USD"})
transaction_service = TransactionService(currency_policy)


@app.post("/transactions")
def create_transaction(transaction: TransactionInput) -> None:
    transaction_service.create_transaction(transaction)
