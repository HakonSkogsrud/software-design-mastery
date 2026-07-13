from models import TransactionInput
from policies import SupportedCurrencyPolicy


class TransactionService:
    def __init__(self, currency_policy: SupportedCurrencyPolicy) -> None:
        self._currency_policy = currency_policy

    def create_transaction(self, transaction: TransactionInput) -> None:
        self._currency_policy.check(transaction.currency)

        print(
            f"Creating transaction for account {transaction.account_id}: "
            f"{transaction.amount} {transaction.currency}"
        )
