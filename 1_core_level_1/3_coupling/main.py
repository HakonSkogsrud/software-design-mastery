from dataclasses import dataclass
from enum import StrEnum


class BookingStatus(StrEnum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Room:
    number: int
    room_type: str
    price: float
    available: bool = True

    def is_available(self) -> bool:
        return self.available

    def mark_unavailable(self) -> None:
        self.available = False

    def mark_available(self) -> None:
        self.available = True


@dataclass
class Booking:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    total_price: float
    status: BookingStatus = BookingStatus.CONFIRMED

    def is_confirmed(self) -> bool:
        return self.status is BookingStatus.CONFIRMED

    def cancel(self) -> None:
        self.status = BookingStatus.CANCELLED

    def change_room(self, new_room_number: int, new_total_price: float) -> None:
        self.room_number = new_room_number
        self.total_price = new_total_price


rooms = {
    101: Room(number=101, room_type="single", price=100),
    102: Room(number=102, room_type="double", price=150),
    201: Room(number=201, room_type="suite", price=250),
}


bookings = []


def calculate_total_price(room, nights, use_discount):
    total_price = room.price * nights

    if use_discount and nights >= 3:
        total_price *= 0.9

    return total_price


def send_booking_confirmation(guest_email, room_number):
    print(f"Sending confirmation email to {guest_email} for room {room_number}")


def validate_booking_request(room_number, nights):
    if room_number not in rooms:
        print("Room does not exist")
        return False

    room = rooms[room_number]

    if not room.available:
        print("Room not available")
        return False

    if nights <= 0:
        print("Invalid number of nights")
        return False

    return True


def book_room(
    guest_name,
    guest_email,
    room_number,
    nights,
    use_discount=False,
    send_confirmation=True,
):
    if not validate_booking_request(room_number, nights):
        return

    room = rooms[room_number]

    total_price = calculate_total_price(room, nights, use_discount)

    booking = Booking(
        guest_name=guest_name,
        guest_email=guest_email,
        room_number=room_number,
        nights=nights,
        total_price=total_price,
    )

    bookings.append(booking)
    room.mark_unavailable()

    print(f"Booked room {room_number} for {guest_name}")

    if send_confirmation:
        send_booking_confirmation(guest_email, room_number)

    return booking


def main() -> None:
    book_room("Alice", "alice@example.com", 101, 2)
    book_room("Bob", "bob@example.com", 102, 3, use_discount=True)
    book_room("Charlie", "charlie@example.com", 101, 1)


if __name__ == "__main__":
    main()
