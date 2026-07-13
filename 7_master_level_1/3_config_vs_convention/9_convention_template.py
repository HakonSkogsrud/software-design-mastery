from dataclasses import dataclass


@dataclass(frozen=True)
class Hotel:
    slug: str


@dataclass(frozen=True)
class Booking:
    id: str
    hotel: Hotel
    guest_email: str


def confirmation_template_for(booking: Booking) -> str:
    return f"{booking.hotel.slug}_confirmation.html"


def send_confirmation_email(booking: Booking) -> None:
    template = confirmation_template_for(booking)

    print(f"Sending confirmation to {booking.guest_email}")
    print(f"Using template: {template}")


def main() -> None:
    booking = Booking(
        id="booking_123",
        hotel=Hotel(slug="grand_hotel"),
        guest_email="guest@example.com",
    )

    send_confirmation_email(booking)


if __name__ == "__main__":
    main()
