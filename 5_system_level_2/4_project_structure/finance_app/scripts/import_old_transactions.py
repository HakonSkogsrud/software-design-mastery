"""Example operational script.

This belongs in scripts/ because it is a one-off operational task.
It can use application code, but application code should not depend on it.
"""

from transactions.sample_data import load_transactions


def main() -> None:
    transactions = load_transactions()
    print(f"Imported {len(transactions)} old transactions")


if __name__ == "__main__":
    main()
