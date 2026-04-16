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

    def is_available(self):
        return self.available

    def mark_unavailable(self):
        self.available = False

    def mark_available(self):
        self.available = True


@dataclass
class Booking:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    total_price: float
    status: BookingStatus = BookingStatus.CONFIRMED

    def is_confirmed(self):
        return self.status is BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CANCELLED

    def change_room(self, new_room_number, new_total_price):
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

bookings: list[Booking] = []


class PricingService:
    def calculate_total_price(self, room, nights, use_discount):
        print("[PricingService] Calculating total price")

        total_price = room.price * nights
        if use_discount and nights >= 3:
            total_price *= 0.9

        return total_price


class AvailabilityService:
    def can_book(self, room_number, nights):
        print("[AvailabilityService] Validating booking request")

        if room_number not in rooms:
            print("Room does not exist")
            return False

        room = rooms[room_number]

        if not room.is_available():
            print("Room not available")
            return False

        if nights <= 0:
            print("Invalid number of nights")
            return False

        return True


class BookingPolicy:
    def initial_status(self, room):
        print("[BookingPolicy] Determining initial booking status")

        if room.room_type == "suite":
            return BookingStatus.PENDING

        return BookingStatus.CONFIRMED


class NotificationService:
    def send_booking_confirmation(self, booking):
        print("[NotificationService] Sending confirmation")
        print(
            f"Sending confirmation email to {booking.guest_email} "
            f"for room {booking.room_number}"
        )


class BookingService:
    def __init__(
        self,
        availability_service: AvailabilityService,
        pricing_service: PricingService,
        booking_policy: BookingPolicy,
        notification_service: NotificationService,
    ):
        self.availability_service = availability_service
        self.pricing_service = pricing_service
        self.booking_policy = booking_policy
        self.notification_service = notification_service

    def book_room(self, booking_request: BookingRequest):
        print("[BookingService] Starting booking flow")

        if not self.availability_service.can_book(
            booking_request.room_number,
            booking_request.nights,
        ):
            return None

        room = rooms[booking_request.room_number]

        total_price = self.pricing_service.calculate_total_price(
            room,
            booking_request.nights,
            booking_request.use_discount,
        )

        booking = Booking(
            guest_name=booking_request.guest_name,
            guest_email=booking_request.guest_email,
            room_number=booking_request.room_number,
            nights=booking_request.nights,
            total_price=total_price,
            status=self.booking_policy.initial_status(room),
        )

        bookings.append(booking)
        room.mark_unavailable()

        print(f"[BookingService] Booked room {room.number} for {booking.guest_name}")

        if booking_request.send_confirmation and booking.is_confirmed():
            self.notification_service.send_booking_confirmation(booking)

        return booking


def main():
    availability_service = AvailabilityService()
    pricing_service = PricingService()
    booking_policy = BookingPolicy()
    notification_service = NotificationService()

    booking_service = BookingService(
        availability_service=availability_service,
        pricing_service=pricing_service,
        booking_policy=booking_policy,
        notification_service=notification_service,
    )

    print("=== Scenario 1: Successful booking ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Alice",
            guest_email="alice@example.com",
            room_number=101,
            nights=2,
        )
    )
    print(f"Booking result: {booking}")
    print()

    print("=== Scenario 2: Room already booked ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Bob",
            guest_email="bob@example.com",
            room_number=101,
            nights=2,
        )
    )
    print(f"Booking result: {booking}")
    print()

    print("=== Scenario 3: Discount applied ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Charlie",
            guest_email="charlie@example.com",
            room_number=102,
            nights=4,
            use_discount=True,
        )
    )
    print(f"Booking result: {booking}")
    print()

    print("=== Scenario 4: Suite starts as pending ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Dana",
            guest_email="dana@example.com",
            room_number=201,
            nights=2,
        )
    )
    print(f"Booking result: {booking}")
    print()


if __name__ == "__main__":
    main()
