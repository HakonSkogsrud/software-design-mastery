from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Iterable

# --- Domain Types ---

type GuestName = str
type GuestEmail = str
type RoomNumber = int


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# --- Domain Model ---


@dataclass
class Booking:
    guest_name: GuestName
    guest_email: GuestEmail
    room_number: RoomNumber
    nights: int
    _total_price: Decimal
    _status: BookingStatus

    def __post_init__(self) -> None:
        if not self.guest_name.strip():
            raise ValueError("Guest name cannot be empty")

        if "@" not in self.guest_email:
            raise ValueError("Invalid email address")

        if self.nights <= 0:
            raise ValueError("Nights must be at least 1")

        if self._total_price < 0:
            raise ValueError("Total price cannot be negative")

    # --- Controlled construction ---

    @classmethod
    def create(
        cls,
        *,
        guest_name: GuestName,
        guest_email: GuestEmail,
        room_number: RoomNumber,
        nights: int,
        total_price: Decimal,
    ) -> "Booking":
        return cls(
            guest_name=guest_name,
            guest_email=guest_email,
            room_number=room_number,
            nights=nights,
            _total_price=total_price,
            _status=BookingStatus.PENDING,
        )

    # --- Read-only access ---

    @property
    def status(self) -> BookingStatus:
        return self._status

    @property
    def total_price(self) -> Decimal:
        return self._total_price

    # --- Behavior (state transitions) ---

    def confirm(self) -> None:
        if self._status is not BookingStatus.PENDING:
            raise ValueError("Only pending bookings can be confirmed")
        self._status = BookingStatus.CONFIRMED

    def cancel(self) -> None:
        if self._status not in {
            BookingStatus.PENDING,
            BookingStatus.CONFIRMED,
        }:
            raise ValueError("Only pending or confirmed bookings can be cancelled")
        self._status = BookingStatus.CANCELLED


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
    def __init__(self, booking_repository: BookingRepository) -> None:
        self._booking_repository = booking_repository

    def create_booking(
        self,
        guest_name: GuestName,
        guest_email: GuestEmail,
        room_number: RoomNumber,
        nights: int,
        price_per_night: Decimal,
    ) -> Booking:
        total_price = price_per_night * nights

        booking = Booking.create(
            guest_name=guest_name,
            guest_email=guest_email,
            room_number=room_number,
            nights=nights,
            total_price=total_price,
        )

        self._booking_repository.save(booking)
        return booking


# --- Example Function ---


def total_revenue(bookings: Iterable[Booking]) -> Decimal:
    total = Decimal("0.00")
    for booking in bookings:
        if booking.status is not BookingStatus.CANCELLED:
            total += booking.total_price
    return total


# --- Entry Point ---


def main() -> None:
    repository = BookingRepository()
    service = BookingService(repository)

    booking = service.create_booking(
        guest_name="Alice Johnson",
        guest_email="alice@example.com",
        room_number=101,
        nights=3,
        price_per_night=Decimal("140.00"),
    )

    print("Created:", booking)

    booking.confirm()
    print("After confirmation:", booking)

    booking.cancel()
    print("After cancellation:", booking)

    print("All bookings:", repository.all())
    print("Total revenue:", total_revenue(repository.all()))


if __name__ == "__main__":
    main()
