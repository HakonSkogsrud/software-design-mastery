from typing import Iterable

from domain import Booking, BookingStatus, Room


class InMemoryBookingRepository:
    def __init__(self) -> None:
        self.rooms: dict[int, Room] = {
            101: Room(number=101, room_type="single", price_per_night=100),
            102: Room(number=102, room_type="double", price_per_night=150),
            201: Room(number=201, room_type="suite", price_per_night=250),
            301: Room(number=301, room_type="suite", price_per_night=320),
        }
        self.bookings: list[Booking] = []

    def get_room(self, room_number: int) -> Room | None:
        return self.rooms.get(room_number)

    def list_rooms(self) -> Iterable[Room]:
        return self.rooms.values()

    def save_booking(self, booking: Booking) -> None:
        self.bookings.append(booking)

    def list_bookings(self) -> list[Booking]:
        return list(self.bookings)

    def find_booking(self, guest_email: str, room_number: int) -> Booking | None:
        for booking in self.bookings:
            if (
                booking.guest_email == guest_email
                and booking.room_number == room_number
            ):
                return booking
        return None

    def active_booking_exists_for_room(self, room_number: int) -> bool:
        for booking in self.bookings:
            if (
                booking.room_number == room_number
                and booking.status is BookingStatus.CONFIRMED
            ):
                return True
        return False
