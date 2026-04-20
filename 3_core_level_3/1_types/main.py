from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Room:
    number: int
    room_type: str
    price: Decimal


ROOMS = {
    101: Room(number=101, room_type="single", price=Decimal("90.00")),
    102: Room(number=102, room_type="double", price=Decimal("140.00")),
    201: Room(number=201, room_type="suite", price=Decimal("220.00")),
}


@dataclass
class Booking:
    booking_id: str
    guest_name: str
    room_type: str
    check_in: date
    check_out: date
    guest_count: int
    status: str
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


class BookingService:
    def __init__(self, pricing_policy) -> None:
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name,
        room_number,
        check_in,
        check_out,
        guest_count,
    ):
        room = ROOMS.get(room_number)

        if room is None:
            raise ValueError("Room does not exist")

        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")

        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")

        total_price = self._pricing_policy.calculate_price(
            room.room_type,  # leaking primitive again
            check_in,
            check_out,
            guest_count,
        )

        booking = Booking(
            booking_id="generated-id",
            guest_name=guest_name,
            room_type=room.room_type,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
            status="pending",
            total_price=total_price,
        )

        return booking


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
