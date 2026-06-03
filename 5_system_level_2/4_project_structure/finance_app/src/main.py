from reports.presentation import print_report
from reports.spending import generate_spending_report
from transactions.filters import filter_transactions_by_month
from transactions.sample_data import load_transactions


def main() -> None:
    transactions = load_transactions()

    may_transactions = filter_transactions_by_month(
        transactions,
        year=2026,
        month=5,
    )

    report = generate_spending_report(may_transactions)

    print_report(report)


if __name__ == "__main__":
    main()
