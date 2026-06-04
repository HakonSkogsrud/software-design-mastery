from bank_sync import BankApiClient, sync_bank_transactions
from domain.events import TransactionCreated
from domain.use_cases import generate_monthly_spending_report
from event_bus_adapter import InMemoryEventBus
from event_handlers import (
    refresh_budget_handler,
    send_notification_handler,
    send_webhook_handler,
)
from main import serialize_event
from transaction_db_adapter import (
    DatabaseTransactionRepository,
    SyncDBTransactionRepository,
)


def print_report() -> None:
    repository = SyncDBTransactionRepository(DatabaseTransactionRepository())
    event_bus = InMemoryEventBus()

    event_bus.subscribe(TransactionCreated, refresh_budget_handler)
    event_bus.subscribe(TransactionCreated, send_notification_handler)
    event_bus.subscribe(TransactionCreated, send_webhook_handler)

    sync_bank_transactions(
        BankApiClient(),
        repository,
        event_bus,
    )

    report = generate_monthly_spending_report(
        repository,
        year=2026,
        month=5,
    )

    print()
    print("Spending report")
    print("---------------")
    print(f"Total spent: EUR {report.total_spent}")
    print(f"Transactions: {report.transaction_count}")

    for category, total in report.totals_by_category.items():
        print(f"- {category}: EUR {total}")

    print()
    print("Event history")
    print("-------------")

    for event in event_bus.list_events():
        print(serialize_event(event))


if __name__ == "__main__":
    print_report()
