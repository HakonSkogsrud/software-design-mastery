from decimal import Decimal


def calculate_cancellation_fee(days_before_check_in: int) -> Decimal:
    if days_before_check_in >= 30:
        return Decimal("0")

    if days_before_check_in >= 7:
        return Decimal("50")

    return Decimal("100")


def main() -> None:
    fee = calculate_cancellation_fee(days_before_check_in=5)
    print(f"Cancellation fee: {fee}")


if __name__ == "__main__":
    main()
