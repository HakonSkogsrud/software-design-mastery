from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Protocol


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Room:
    number: int
    room_type: str
    price: Decimal
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
    total_price: Decimal
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
    preferred_channel: str = "email"
    is_corporate: bool = False
    requires_invoice: bool = False


class BookingRepository(Protocol):
    def get_room(self, room_number: int) -> Room | None: ...

    def save_booking(self, booking: Booking) -> None: ...

    def active_booking_exists_for_room(self, room_number: int) -> bool: ...

    def list_bookings(self) -> list[Booking]: ...


class Logger:
    def log(self, message):
        print(f"[LOG] {message}")


class RetryPolicy:
    def retry_count(self):
        return 3


class InMemoryBookingRepository:
    def __init__(self, rooms):
        self._rooms = {room.number: room for room in rooms}
        self._bookings = []

    def get_room(self, room_number):
        return self._rooms.get(room_number)

    def save_booking(self, booking):
        self._bookings.append(booking)

    def active_booking_exists_for_room(self, room_number):
        return any(
            booking.room_number == room_number
            and booking.status is not BookingStatus.CANCELLED
            for booking in self._bookings
        )

    def list_bookings(self):
        return list(self._bookings)


class AvailabilityService:
    def can_book(self, room, nights):
        print("[AvailabilityService] Validating booking request")

        if room is None:
            print("Room does not exist")
            return False

        if not room.is_available():
            print("Room not available")
            return False

        if nights <= 0:
            print("Invalid number of nights")
            return False

        return True


class PricingService:
    def __init__(self, logger):
        self.logger = logger

    def calculate_total_price(
        self,
        room,
        nights,
        use_discount,
        is_corporate,
        requires_invoice,
    ):
        self.logger.log("Calculating total price")

        total_price = room.price * nights

        if use_discount and nights >= 3:
            total_price *= Decimal("0.9")

        if is_corporate:
            total_price *= Decimal("0.95")

        if requires_invoice and not is_corporate:
            total_price += Decimal("12.50")

        return total_price


class BookingPolicy:
    def __init__(self, logger):
        self.logger = logger

    def initial_status(self, room):
        self.logger.log("Determining initial booking status")

        if room.room_type == "suite":
            return BookingStatus.PENDING

        return BookingStatus.CONFIRMED


class NotificationService:
    def __init__(self, logger, retry_policy):
        self.logger = logger
        self.retry_policy = retry_policy

    def send_booking_confirmation(self, booking, preferred_channel):
        self.logger.log(
            f"Sending confirmation with up to {self.retry_policy.retry_count()} retries"
        )
        print(
            f"Sending confirmation via {preferred_channel} "
            f"to {booking.guest_email} for room {booking.room_number}"
        )


class BookingService:
    def __init__(
        self,
        repository: BookingRepository,
        availability_service,
        pricing_service,
        booking_policy,
        notification_service,
    ):
        self.repository = repository
        self.availability_service = availability_service
        self.pricing_service = pricing_service
        self.booking_policy = booking_policy
        self.notification_service = notification_service

    def book_room(self, booking_request):
        print("[BookingService] Starting booking flow")

        room = self.repository.get_room(booking_request.room_number)

        if not self.availability_service.can_book(room, booking_request.nights):
            return None

        if self.repository.active_booking_exists_for_room(room.number):
            print("Room already has an active booking")
            return None

        total_price = self.pricing_service.calculate_total_price(
            room=room,
            nights=booking_request.nights,
            use_discount=booking_request.use_discount,
            is_corporate=booking_request.is_corporate,
            requires_invoice=booking_request.requires_invoice,
        )

        booking = Booking(
            guest_name=booking_request.guest_name,
            guest_email=booking_request.guest_email,
            room_number=booking_request.room_number,
            nights=booking_request.nights,
            total_price=total_price,
            status=self.booking_policy.initial_status(room),
        )

        self.repository.save_booking(booking)
        room.mark_unavailable()

        print(f"[BookingService] Booked room {room.number} for {booking.guest_name}")

        if booking_request.send_confirmation and booking.is_confirmed():
            self.notification_service.send_booking_confirmation(
                booking,
                booking_request.preferred_channel,
            )

        return booking


def main():
    logger = Logger()
    retry_policy = RetryPolicy()

    repository = InMemoryBookingRepository(
        rooms=[
            Room(number=101, room_type="single", price=Decimal("100")),
            Room(number=102, room_type="double", price=Decimal("150")),
            Room(number=201, room_type="suite", price=Decimal("250")),
        ]
    )
    availability_service = AvailabilityService()
    pricing_service = PricingService(logger)
    booking_policy = BookingPolicy(logger)
    notification_service = NotificationService(logger, retry_policy)

    booking_service = BookingService(
        repository=repository,
        availability_service=availability_service,
        pricing_service=pricing_service,
        booking_policy=booking_policy,
        notification_service=notification_service,
    )

    print("=== Scenario 1: Standard booking ===")
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

    print("=== Scenario 2: Corporate booking ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Bob",
            guest_email="bob@company.com",
            room_number=102,
            nights=2,
            is_corporate=True,
            requires_invoice=True,
            preferred_channel="email",
        )
    )
    print(f"Booking result: {booking}")
    print()

    print("=== Scenario 3: Suite booking starts as pending ===")
    booking = booking_service.book_room(
        BookingRequest(
            guest_name="Charlie",
            guest_email="charlie@example.com",
            room_number=201,
            nights=4,
            use_discount=True,
            requires_invoice=True,
            send_confirmation=False,
        )
    )
    print(f"Booking result: {booking}")
    print()

    print("=== Saved bookings ===")
    for saved_booking in repository.list_bookings():
        print(saved_booking)


if __name__ == "__main__":
    main()
