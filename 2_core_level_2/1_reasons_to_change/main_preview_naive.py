from dataclasses import dataclass
from enum import StrEnum


class BookingStatus(StrEnum):
    PENDING = "pending"
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


@dataclass
class BookingRequest:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    use_discount: bool = False
    send_confirmation: bool = True


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


def preview_booking(room_number, nights, use_discount=False):
    if room_number not in rooms:
        print("Room does not exist")
        return

    if nights <= 0:
        print("Invalid number of nights")
        return

    room = rooms[room_number]
    total_price = calculate_total_price(room, nights, use_discount)

    status = BookingStatus.CONFIRMED
    if room.room_type == "suite":
        status = BookingStatus.PENDING

    print("Preview:")
    print(f"Room {room.number} ({room.room_type})")
    print(f"Nights: {nights}")
    print(f"Total price: {total_price}")
    print(f"Initial status: {status}")


def book_room(booking_request: BookingRequest):
    if not validate_booking_request(
        booking_request.room_number, booking_request.nights
    ):
        return

    room = rooms[booking_request.room_number]

    total_price = calculate_total_price(
        room, booking_request.nights, booking_request.use_discount
    )

    status = BookingStatus.CONFIRMED
    if room.room_type == "suite":
        status = BookingStatus.PENDING

    booking = Booking(
        guest_name=booking_request.guest_name,
        guest_email=booking_request.guest_email,
        room_number=booking_request.room_number,
        nights=booking_request.nights,
        total_price=total_price,
        status=status,
    )

    bookings.append(booking)
    room.mark_unavailable()

    print(f"Booked room {booking_request.room_number} for {booking_request.guest_name}")

    if booking_request.send_confirmation and booking.is_confirmed():
        send_booking_confirmation(
            booking_request.guest_email, booking_request.room_number
        )

    return booking


def upgrade_room(guest_email, current_room, new_room):
    if new_room not in rooms:
        print("New room does not exist")
        return

    if not rooms[new_room].is_available():
        print("New room is not available")
        return

    for booking in bookings:
        if booking.guest_email == guest_email and booking.room_number == current_room:
            if booking.status != BookingStatus.CONFIRMED:
                print("Only confirmed bookings can be upgraded")
                return

            old_price = rooms[current_room].price * booking.nights
            new_price = rooms[new_room].price * booking.nights

            booking.change_room(new_room, new_price)

            rooms[current_room].mark_available()
            rooms[new_room].mark_unavailable()

            print(
                f"Upgraded booking for {guest_email} from room {current_room} to {new_room}"
            )
            print(f"Additional charge: ${new_price - old_price}")

            return

    print("Booking not found")


def main() -> None:
    preview_booking(201, 2)
    print()

    book_room(
        BookingRequest(
            guest_name="Alice",
            guest_email="alice@example.com",
            room_number=101,
            nights=2,
        )
    )
    print()

    book_room(
        BookingRequest(
            guest_name="Bob",
            guest_email="bob@example.com",
            room_number=201,
            nights=2,
        )
    )


if __name__ == "__main__":
    main()
