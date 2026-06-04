from domain.events import TransactionCreated


def refresh_budget_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Refreshing budget for category {event.category}")


def send_notification_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(
        f"Sending notification: {event.description} ({event.amount} {event.currency})"
    )


def send_webhook_handler(event: object) -> None:
    if not isinstance(event, TransactionCreated):
        return

    print(f"Sending webhook for TransactionCreated: {event.transaction_id}")
