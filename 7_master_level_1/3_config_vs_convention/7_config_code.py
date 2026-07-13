from dataclasses import dataclass
from decimal import Decimal
from typing import Any

CONFIG = {
    "cancellation_policy": [
        {"days_before": 30, "fee": "0"},
        {"days_before": 7, "fee": "50"},
        {"days_before": 0, "fee": "100"},
    ]
}


@dataclass(frozen=True)
class CancellationRule:
    days_before: int
    fee: Decimal


def load_cancellation_rules(config: dict[str, Any]) -> list[CancellationRule]:
    return [
        CancellationRule(
            days_before=entry["days_before"],
            fee=Decimal(entry["fee"]),
        )
        for entry in config["cancellation_policy"]
    ]


def calculate_cancellation_fee(
    days_before_check_in: int,
    rules: list[CancellationRule],
) -> Decimal:
    for rule in sorted(rules, key=lambda rule: rule.days_before, reverse=True):
        if days_before_check_in >= rule.days_before:
            return rule.fee

    raise ValueError("No cancellation rule matched.")


def main() -> None:
    rules = load_cancellation_rules(CONFIG)

    fee = calculate_cancellation_fee(
        days_before_check_in=5,
        rules=rules,
    )

    print(f"Cancellation fee: {fee}")


if __name__ == "__main__":
    main()
