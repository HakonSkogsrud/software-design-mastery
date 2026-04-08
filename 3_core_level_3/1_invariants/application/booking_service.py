from datetime import date
from uuid import uuid4

from domain.booking import Booking
from ports.booking_repository import BookingRepository
from ports.pricing_policy import PricingPolicy


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        pricing_policy: PricingPolicy,
    ) -> None:
        self._booking_repository = booking_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name: str,
        room_type: str,
        check_in: date,
        check_out: date,
        guest_count: int,
    ) -> Booking:
        self._validate_guest_name(guest_name)
        self._validate_room_type(room_type)
        self._validate_stay_dates(check_in, check_out)
        self._validate_guest_count(guest_count)
        self._validate_room_capacity(room_type, guest_count)

        total_price = self._pricing_policy.calculate_price(
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
        )

        booking = Booking(
            booking_id=str(uuid4()),
            guest_name=guest_name,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
            status="pending",
            total_price=total_price,
        )

        self._booking_repository.save(booking)
        return booking

    def confirm_booking(self, booking_id: str) -> None:
        booking = self._booking_repository.get(booking_id)

        if booking is None:
            raise ValueError(f"Booking {booking_id} not found")

        if booking.status != "pending":
            raise ValueError("Only pending bookings can be confirmed")

        booking.status = "confirmed"
        self._booking_repository.save(booking)

    def cancel_booking(self, booking_id: str) -> None:
        booking = self._booking_repository.get(booking_id)

        if booking is None:
            raise ValueError(f"Booking {booking_id} not found")

        if booking.status not in {"pending", "confirmed"}:
            raise ValueError("Only pending or confirmed bookings can be canceled")

        booking.status = "canceled"
        self._booking_repository.save(booking)

    def _validate_guest_name(self, guest_name: str) -> None:
        if not guest_name.strip():
            raise ValueError("Guest name cannot be empty")

    def _validate_room_type(self, room_type: str) -> None:
        allowed_room_types = {"single", "double", "suite"}
        if room_type not in allowed_room_types:
            raise ValueError(f"Invalid room type: {room_type}")

    def _validate_stay_dates(self, check_in: date, check_out: date) -> None:
        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")

    def _validate_guest_count(self, guest_count: int) -> None:
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")

    def _validate_room_capacity(self, room_type: str, guest_count: int) -> None:
        max_capacity_by_room_type = {
            "single": 1,
            "double": 2,
            "suite": 4,
        }

        max_capacity = max_capacity_by_room_type[room_type]

        if guest_count > max_capacity:
            raise ValueError(
                f"{room_type.capitalize()} room cannot hold {guest_count} guests"
            )
