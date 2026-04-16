from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Iterable

# --- Domain Types ---

type BookingId = str
type GuestName = str


class RoomType(StrEnum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"


@dataclass(frozen=True, slots=True)
class GuestCount:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("Guest count must be at least 1")


@dataclass(frozen=True, slots=True)
class Period:
    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        if self.check_out <= self.check_in:
            raise ValueError("Check-out must be after check-in")

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# --- Domain Model ---


@dataclass
class Booking:
    booking_id: BookingId
    guest_name: GuestName
    room_type: RoomType
    period: Period
    guest_count: GuestCount
    status: BookingStatus
    total_price: Decimal

    def __post_init__(self) -> None:
        if not self.guest_name.strip():
            raise ValueError("Guest name cannot be empty")

        if self.total_price < 0:
            raise ValueError("Total price cannot be negative")

    def confirm(self) -> None:
        if self.status is not BookingStatus.PENDING:
            raise ValueError("Only pending bookings can be confirmed")
        self.status = BookingStatus.CONFIRMED

    def cancel(self) -> None:
        if self.status not in {
            BookingStatus.PENDING,
            BookingStatus.CONFIRMED,
        }:
            raise ValueError("Only pending or confirmed bookings can be cancelled")
        self.status = BookingStatus.CANCELLED


# --- Pricing Policy ---


class PricingPolicy:
    def calculate_price(
        self,
        room_type: RoomType,
        period: Period,
        guest_count: GuestCount,
    ) -> Decimal:
        base_prices: dict[RoomType, Decimal] = {
            RoomType.SINGLE: Decimal("90.00"),
            RoomType.DOUBLE: Decimal("140.00"),
            RoomType.SUITE: Decimal("220.00"),
        }

        total = base_prices[room_type] * period.nights

        if guest_count.value > 2:
            total += Decimal("20.00") * (guest_count.value - 2) * period.nights

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
        room_type: str,
        check_in: date,
        check_out: date,
        guest_count: int,
    ) -> Booking:
        period = Period(check_in=check_in, check_out=check_out)
        validated_guest_count = GuestCount(guest_count)
        validated_room_type = RoomType(room_type)

        total_price = self._pricing_policy.calculate_price(
            room_type=validated_room_type,
            period=period,
            guest_count=validated_guest_count,
        )

        booking = Booking(
            booking_id="generated-id",
            guest_name=guest_name,
            room_type=validated_room_type,
            period=period,
            guest_count=validated_guest_count,
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
