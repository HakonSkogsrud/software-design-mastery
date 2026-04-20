from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Iterable

type BookingId = str
type GuestName = str
type RoomNumber = int


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("Guest email must be valid")


@dataclass(frozen=True, slots=True)
class StayNights:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("Nights must be at least 1")


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.amount * multiplier)


@dataclass
class Room:
    number: RoomNumber
    room_type: str
    price_per_night: Money


@dataclass
class Booking:
    booking_id: BookingId
    guest_name: GuestName
    guest_email: EmailAddress
    room_number: RoomNumber
    nights: StayNights
    total_price: Money
    status: BookingStatus = BookingStatus.PENDING

    def __post_init__(self) -> None:
        if not self.guest_name.strip():
            raise ValueError("Guest name cannot be empty")


class RoomRepository:
    def __init__(self) -> None:
        self._rooms: dict[RoomNumber, Room] = {
            101: Room(
                number=101,
                room_type="single",
                price_per_night=Money(Decimal("100.00")),
            ),
            102: Room(
                number=102,
                room_type="double",
                price_per_night=Money(Decimal("140.00")),
            ),
            201: Room(
                number=201,
                room_type="suite",
                price_per_night=Money(Decimal("220.00")),
            ),
        }

    def get(self, room_number: RoomNumber) -> Room | None:
        return self._rooms.get(room_number)

    def all(self) -> list[Room]:
        return list(self._rooms.values())


class BookingRepository:
    def __init__(self) -> None:
        self._bookings: list[Booking] = []

    def save(self, booking: Booking) -> None:
        self._bookings.append(booking)

    def all(self) -> list[Booking]:
        return self._bookings


class PricingPolicy:
    def calculate_total_price(self, room: Room, nights: StayNights) -> Money:
        return room.price_per_night * nights.value


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
        pricing_policy: PricingPolicy,
    ) -> None:
        self._booking_repository = booking_repository
        self._room_repository = room_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        booking_id: BookingId,
        guest_name: GuestName,
        guest_email: str,
        room_number: RoomNumber,
        nights: int,
    ) -> Booking:
        room = self._room_repository.get(room_number)
        if room is None:
            raise ValueError("Room does not exist")

        validated_email = EmailAddress(guest_email)
        validated_nights = StayNights(nights)

        total_price = self._pricing_policy.calculate_total_price(
            room=room,
            nights=validated_nights,
        )

        booking = Booking(
            booking_id=booking_id,
            guest_name=guest_name,
            guest_email=validated_email,
            room_number=room.number,
            nights=validated_nights,
            total_price=total_price,
        )

        self._booking_repository.save(booking)
        return booking


def total_revenue(bookings: Iterable[Booking]) -> Money:
    total = Money(Decimal("0.00"))
    for booking in bookings:
        if booking.status is not BookingStatus.CANCELLED:
            total = total + booking.total_price
    return total


def main() -> None:
    booking_repository = BookingRepository()
    room_repository = RoomRepository()
    pricing_policy = PricingPolicy()

    booking_service = BookingService(
        booking_repository=booking_repository,
        room_repository=room_repository,
        pricing_policy=pricing_policy,
    )

    booking = booking_service.create_booking(
        booking_id="BKG-001",
        guest_name="Alice Johnson",
        guest_email="alice@example.com",
        room_number=101,
        nights=3,
    )

    print("Created:", booking)
    print("Rooms:", room_repository.all())
    print("All bookings:", booking_repository.all())
    print("Total revenue:", total_revenue(booking_repository.all()).amount)


if __name__ == "__main__":
    main()
