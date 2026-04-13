rooms = {
    101: {"type": "single", "price": 100, "available": True},
    102: {"type": "double", "price": 150, "available": True},
    201: {"type": "suite", "price": 250, "available": True},
}

bookings = []


def calculate_total_price(room, nights, use_discount):
    total_price = room["price"] * nights

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

    if not room["available"]:
        print("Room not available")
        return False

    if nights <= 0:
        print("Invalid number of nights")
        return False

    return True


def build_booking(guest_name, guest_email, room_number, nights, total_price):
    return {
        "guest_name": guest_name,
        "guest_email": guest_email,
        "room_number": room_number,
        "nights": nights,
        "total_price": total_price,
        "status": "confirmed",
    }


def mark_room_unavailable(room_number):
    rooms[room_number]["available"] = False


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

    booking = build_booking(guest_name, guest_email, room_number, nights, total_price)

    bookings.append(booking)
    mark_room_unavailable(room_number)

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
