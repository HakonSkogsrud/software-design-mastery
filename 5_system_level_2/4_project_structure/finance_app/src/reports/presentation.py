from .models import SpendingReport


def print_report(report: SpendingReport) -> None:
    print("Spending report")
    print("---------------")
    print(f"Total spent: €{report.total_spent}")
    print(f"Transactions: {report.transaction_count}")
    print()

    print("By category:")
    for category, total in report.totals_by_category.items():
        print(f"- {category}: €{total}")
