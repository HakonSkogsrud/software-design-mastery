from domain.booking import Booking
from ports.booking_repository import BookingRepository


class InMemoryBookingRepository(BookingRepository):
    def __init__(self) -> None:
        self._bookings: dict[str, Booking] = {}

    def save(self, booking: Booking) -> None:
        self._bookings[booking.booking_id] = booking

    def get(self, booking_id: str) -> Booking | None:
        return self._bookings.get(booking_id)
