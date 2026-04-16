from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Booking:
    booking_id: str
    guest_name: str
    room_type: str
    check_in: date
    check_out: date
    guest_count: int
    status: BookingStatus
    total_price: Decimal


class PricingPolicy:
    def calculate_price(
        self,
        room_type,
        check_in,
        check_out,
        guest_count,
    ):
        nights = (check_out - check_in).days

        base_prices = {
            "single": Decimal("90.00"),
            "double": Decimal("140.00"),
            "suite": Decimal("220.00"),
        }

        base_price = base_prices[room_type]
        total = base_price * nights

        if guest_count > 2:
            total += Decimal("20.00") * (guest_count - 2) * nights

        return total


class BookingRepository:
    def __init__(self) -> None:
        self._bookings = []

    def save(self, booking) -> None:
        self._bookings.append(booking)

    def all(self):
        return self._bookings


class BookingService:
    def __init__(self, booking_repository, pricing_policy) -> None:
        self._booking_repository = booking_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name,
        room_type,
        check_in,
        check_out,
        guest_count,
    ):
        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")

        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")

        total_price = self._pricing_policy.calculate_price(
            room_type,
            check_in,
            check_out,
            guest_count,
        )

        booking = Booking(
            booking_id="generated-id",
            guest_name=guest_name,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
            status=BookingStatus.PENDING,
            total_price=total_price,
        )

        self._booking_repository.save(booking)
        return booking


def main() -> None:
    repository = BookingRepository()
    pricing_policy = PricingPolicy()
    booking_service = BookingService(repository, pricing_policy)

    booking = booking_service.create_booking(
        guest_name="Alice Johnson",
        room_type="double",
        check_in=date(2026, 5, 10),
        check_out=date(2026, 5, 14),
        guest_count=2,
    )

    print(booking)
    print(repository.all())


if __name__ == "__main__":
    main()
