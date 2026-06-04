from .errors import NoTransactionsForPeriodError
from .event_port import EventBus
from .events import TransactionCreated
from .models import SpendingReport, Transaction
from .transaction_logic import (
    calculate_spending_by_category,
    calculate_total_spending,
    filter_transactions_by_month,
)
from .transaction_port import TransactionRepository


def create_transaction(
    transaction: Transaction,
    repository: TransactionRepository,
    event_bus: EventBus,
) -> None:
    repository.add(transaction)
    event_bus.publish(TransactionCreated.from_transaction(transaction))


def generate_monthly_spending_report(
    repository: TransactionRepository,
    year: int,
    month: int,
) -> SpendingReport:
    transactions = repository.list_all()

    monthly_transactions = filter_transactions_by_month(
        transactions,
        year=year,
        month=month,
    )

    if not monthly_transactions:
        raise NoTransactionsForPeriodError(
            message="No transactions found",
            month=month,
            year=year,
        )

    return SpendingReport(
        total_spent=calculate_total_spending(monthly_transactions),
        totals_by_category=calculate_spending_by_category(monthly_transactions),
        transaction_count=len(monthly_transactions),
    )
