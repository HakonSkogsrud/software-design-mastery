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
        return None

    room = rooms[room_number]

    if not room["available"]:
        print("Room not available")
        return None

    if nights <= 0:
        print("Invalid number of nights")
        return None

    # --- Pricing logic ---
    total_price = room["price"] * nights
    discount_amount = 0.0

    if use_discount:
        if nights >= 3 and room["type"] in {"double", "suite"}:
            discount_amount = total_price * 0.1
            total_price -= discount_amount

    # --- Booking creation ---
    booking = {
        "guest_name": guest_name,
        "guest_email": guest_email,
        "room_number": room_number,
        "nights": nights,
        "total_price": total_price,
        "discount_amount": discount_amount,  # new field
        "status": "confirmed",
    }

    bookings.append(booking)
    room["available"] = False

    print(f"Booked room {room_number} for {guest_name}")

    # --- Notification logic ---
    if send_confirmation:
        if discount_amount > 0:
            print(
                f"Sending confirmation email to {guest_email} "
                f"(you saved ${discount_amount:.2f})"
            )
        else:
            print(f"Sending confirmation email to {guest_email}...")

    return booking


def main() -> None:
    book_room("Alice", "alice@example.com", 101, 2)
    book_room("Bob", "bob@example.com", 102, 3, use_discount=True)
    book_room("Charlie", "charlie@example.com", 101, 1)


if __name__ == "__main__":
    main()
