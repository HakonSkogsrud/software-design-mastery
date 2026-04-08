from typing import Protocol

from domain.booking import Booking


class BookingRepository(Protocol):
    def save(self, booking: Booking) -> None: ...

    def get(self, booking_id: str) -> Booking | None: ...
