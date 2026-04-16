from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Iterable

# --- Type Aliases ---

type BookingId = str
type GuestName = str
type RoomType = str
type GuestCount = int


# --- Domain Models ---


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Booking:
    booking_id: BookingId
    guest_name: GuestName
    room_type: RoomType
    check_in: date
    check_out: date
    guest_count: GuestCount
    status: BookingStatus
    total_price: Decimal


# --- Pricing Policy ---


class PricingPolicy:
    def calculate_price(
        self,
        room_type: RoomType,
        check_in: date,
        check_out: date,
        guest_count: GuestCount,
    ) -> Decimal:
        nights = (check_out - check_in).days

        base_prices: dict[RoomType, Decimal] = {
            "single": Decimal("90.00"),
            "double": Decimal("140.00"),
            "suite": Decimal("220.00"),
        }

        base_price = base_prices[room_type]
        total = base_price * nights

        if guest_count > 2:
            total += Decimal("20.00") * (guest_count - 2) * nights

        return total


# --- Repository ---


class BookingRepository:
    def __init__(self) -> None:
        self._bookings: list[Booking] = []

    def save(self, booking: Booking) -> None:
        self._bookings.append(booking)

    def all(self) -> list[Booking]:
        return self._bookings


# --- Service ---


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        pricing_policy: PricingPolicy,
    ) -> None:
        self._booking_repository = booking_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name: GuestName,
        room_type: RoomType,
        check_in: date,
        check_out: date,
        guest_count: GuestCount,
    ) -> Booking:
        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")

        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")

        total_price = self._pricing_policy.calculate_price(
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
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


# --- Example Function Using Generic Input ---


def total_revenue(bookings: Iterable[Booking]) -> Decimal:
    total = Decimal("0.00")
    for booking in bookings:
        total += booking.total_price
    return total


# --- Entry Point ---


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
    print("Total revenue:", total_revenue(repository.all()))


if __name__ == "__main__":
    main()
