rooms = {
    101: {"type": "single", "price": 100, "available": True},
    102: {"type": "double", "price": 150, "available": True},
}

bookings = []


def book_room(
    guest_name,
    guest_email,
    room_number,
    nights,
    use_discount=False,
    send_confirmation=True,
):
    if room_number not in rooms:
        print("Room does not exist")
        return

    room = rooms[room_number]

    if not room["available"]:
        print("Room not available")
        return

    if nights <= 0:
        print("Invalid number of nights")
        return

    total_price = room["price"] * nights

    if use_discount:
        if nights >= 3:
            total_price = total_price * 0.9

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
        print(f"Sending confirmation email to {guest_email}...")

    return booking


def main():
    book_room("Alice", "alice@example.com", 101, 2)
    book_room("Bob", "bob@example.com", 102, 3, use_discount=True)
    book_room("Charlie", "charlie@example.com", 101, 1)


if __name__ == "__main__":
    main()
