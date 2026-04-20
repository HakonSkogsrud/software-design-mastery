from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Room:
    number: int
    room_type: str
    price_per_night: Decimal


@dataclass
class Booking:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    total_price: Decimal
    status: BookingStatus = BookingStatus.PENDING


class RoomRepository:
    def __init__(self):
        self._rooms = {
            101: Room(
                number=101, room_type="single", price_per_night=Decimal("100.00")
            ),
            102: Room(
                number=102, room_type="double", price_per_night=Decimal("140.00")
            ),
            201: Room(number=201, room_type="suite", price_per_night=Decimal("220.00")),
        }

    def get(self, room_number):
        return self._rooms.get(room_number)


class BookingRepository:
    def __init__(self):
        self._bookings = []

    def save(self, booking):
        self._bookings.append(booking)

    def all(self):
        return self._bookings


class PricingPolicy:
    def calculate_total_price(self, room, nights):
        return room.price_per_night * nights


class BookingService:
    def __init__(self, booking_repository, room_repository, pricing_policy):
        self._booking_repository = booking_repository
        self._room_repository = room_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name,
        guest_email,
        room_number,
        nights,
    ):
        room = self._room_repository.get(room_number)

        if room is None:
            raise ValueError("Room does not exist")

        if nights <= 0:
            raise ValueError("Nights must be at least 1")

        total_price = self._pricing_policy.calculate_total_price(
            room,
            nights,
        )

        booking = Booking(
            guest_name=guest_name,
            guest_email=guest_email,
            room_number=room.number,
            nights=nights,
            total_price=total_price,
            status=BookingStatus.PENDING,
        )

        self._booking_repository.save(booking)
        return booking


def total_revenue(bookings):
    total = Decimal("0.00")
    for booking in bookings:
        if booking.status is not BookingStatus.CANCELLED:
            total += booking.total_price
    return total


def main():
    booking_repository = BookingRepository()
    room_repository = RoomRepository()
    pricing_policy = PricingPolicy()

    service = BookingService(
        booking_repository,
        room_repository,
        pricing_policy,
    )

    booking = service.create_booking(
        guest_name="Alice Johnson",
        guest_email="alice@example.com",
        room_number=101,
        nights=3,
    )

    print("Created:", booking)
    print("All bookings:", booking_repository.all())
    print("Total revenue:", total_revenue(booking_repository.all()))


if __name__ == "__main__":
    main()
