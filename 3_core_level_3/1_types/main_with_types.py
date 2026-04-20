from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import TypeAlias

BookingId: TypeAlias = str
GuestName: TypeAlias = str
GuestCount: TypeAlias = int


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Room:
    number: int
    room_type: str
    price: Decimal


ROOMS: dict[int, Room] = {
    101: Room(number=101, room_type="single", price=Decimal("90.00")),
    102: Room(number=102, room_type="double", price=Decimal("140.00")),
    201: Room(number=201, room_type="suite", price=Decimal("220.00")),
}


@dataclass
class Booking:
    booking_id: BookingId
    guest_name: GuestName
    room: Room
    check_in: date
    check_out: date
    guest_count: GuestCount
    status: BookingStatus
    total_price: Decimal


class PricingPolicy:
    def calculate_price(
        self,
        room: Room,
        check_in: date,
        check_out: date,
        guest_count: GuestCount,
    ) -> Decimal:
        nights = (check_out - check_in).days
        total = room.price * nights

        if guest_count > 2:
            total += Decimal("20.00") * (guest_count - 2) * nights

        return total


class BookingService:
    def __init__(self, pricing_policy: PricingPolicy) -> None:
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name: GuestName,
        room_number: int,
        check_in: date,
        check_out: date,
        guest_count: GuestCount,
    ) -> Booking:
        room = ROOMS.get(room_number)

        if room is None:
            raise ValueError("Room does not exist")

        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")

        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")

        total_price = self._pricing_policy.calculate_price(
            room=room,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
        )

        booking = Booking(
            booking_id="generated-id",
            guest_name=guest_name,
            room=room,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
            status=BookingStatus.PENDING,
            total_price=total_price,
        )

        return booking


def total_revenue(bookings: Iterable[Booking]) -> Decimal:
    total = Decimal("0.00")
    for booking in bookings:
        total += booking.total_price
    return total


def main() -> None:
    pricing_policy = PricingPolicy()
    booking_service = BookingService(pricing_policy)

    booking = booking_service.create_booking(
        guest_name="Alice Johnson",
        room_number=102,
        check_in=date(2026, 5, 10),
        check_out=date(2026, 5, 14),
        guest_count=2,
    )

    print(booking)


if __name__ == "__main__":
    main()
