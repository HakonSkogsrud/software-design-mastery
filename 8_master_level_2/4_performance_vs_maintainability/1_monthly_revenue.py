from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Booking:
    total_price: Decimal


def calculate_monthly_revenue(
    bookings: list[Booking],
) -> Decimal:
    total = Decimal("0.00")

    for booking in bookings:
        total += booking.total_price

    return total


def main() -> None:
    bookings = [
        Booking(total_price=Decimal("125.00")),
        Booking(total_price=Decimal("240.00")),
        Booking(total_price=Decimal("89.50")),
    ]

    revenue = calculate_monthly_revenue(bookings)

    print(f"Monthly revenue: €{revenue}")


if __name__ == "__main__":
    main()
