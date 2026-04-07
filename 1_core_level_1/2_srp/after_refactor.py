rooms = {
    101: {"type": "single", "price": 100, "available": True},
    102: {"type": "double", "price": 150, "available": True},
    201: {"type": "suite", "price": 250, "available": True},
}

bookings = []


def calculate_price(room: dict, nights: int, use_discount: bool) -> float:
    total = room["price"] * nights

    if use_discount and nights >= 3:
        total *= 0.9

    return total


def send_booking_confirmation(guest_email: str, room_number: int) -> None:
    print(f"Sending confirmation email to {guest_email} for room {room_number}")


def book_room(
    guest_name: str,
    guest_email: str,
    room_number: int,
    nights: int,
    use_discount: bool = False,
    send_confirmation: bool = True,
):
    if room_number not in rooms:
        print("Room does not exist")
        return None

    room = rooms[room_number]

    if not room["available"]:
        print("Room not available")
        return None

    if nights <= 0:
        print("Invalid number of nights")
        return None

    total_price = calculate_price(room, nights, use_discount)

    booking = {
        "guest_name": guest_name,
        "guest_email": guest_email,
        "room_number": room_number,
        "nights": nights,
        "total_price": total_price,
        "status": "confirmed",
    }

    bookings.append(booking)
    room["available"] = False

    print(f"Booked room {room_number} for {guest_name}")

    if send_confirmation:
        send_booking_confirmation(guest_email, room_number)

    return booking


def cancel_booking(guest_email, room_number, refund=False):
    for booking in bookings:
        if (
            booking["guest_email"] == guest_email
            and booking["room_number"] == room_number
        ):
            if booking["status"] == "cancelled":
                print("Booking already cancelled")
                return

            booking["status"] = "cancelled"
            rooms[room_number]["available"] = True

            print(f"Cancelled booking for room {room_number}")

            if refund:
                print(f"Refunding {booking['total_price']} to {guest_email}")

            return

    print("Booking not found")


def get_total_revenue(include_cancelled=False):
    total = 0
    for booking in bookings:
        if include_cancelled:
            total += booking["total_price"]
        else:
            if booking["status"] != "cancelled":
                total += booking["total_price"]
    return total


def show_available_rooms(room_type=None):
    for room_number, room in rooms.items():
        if room["available"]:
            if room_type is None or room["type"] == room_type:
                print(
                    f"Room {room_number}: {room['type']} - ${room['price']} per night"
                )


def upgrade_room(guest_email, current_room, new_room):
    if new_room not in rooms:
        print("New room does not exist")
        return

    if not rooms[new_room]["available"]:
        print("New room is not available")
        return

    for booking in bookings:
        if (
            booking["guest_email"] == guest_email
            and booking["room_number"] == current_room
        ):
            if booking["status"] != "confirmed":
                print("Only confirmed bookings can be upgraded")
                return

            old_price = rooms[current_room]["price"] * booking["nights"]
            new_price = rooms[new_room]["price"] * booking["nights"]

            booking["room_number"] = new_room
            booking["total_price"] = new_price

            rooms[current_room]["available"] = True
            rooms[new_room]["available"] = False

            print(
                f"Upgraded booking for {guest_email} from room {current_room} to {new_room}"
            )
            print(f"Additional charge: ${new_price - old_price}")

            return

    print("Booking not found")


def main() -> None:
    show_available_rooms()
    book_room("Alice", "alice@example.com", 101, 2)
    book_room("Bob", "bob@example.com", 102, 3, use_discount=True)
    book_room("Charlie", "charlie@example.com", 101, 1)

    print(f"Total revenue: {get_total_revenue()}")


if __name__ == "__main__":
    main()
