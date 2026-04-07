from decimal import Decimal

from domain import BookingStatus
from repository import InMemoryBookingRepository


class ReportingService:
    def __init__(self, repository: InMemoryBookingRepository) -> None:
        self.repository = repository

    def total_revenue(self, include_cancelled: bool = False) -> Decimal:
        total = Decimal("0")

        for booking in self.repository.list_bookings():
            if include_cancelled or booking.status is BookingStatus.CONFIRMED:
                total += booking.total_price

        return total

    def occupancy_report(self) -> list[str]:
        lines: list[str] = []

        for room in self.repository.list_rooms():
            status = "available" if room.available else "occupied"
            lines.append(f"Room {room.number} ({room.room_type}): {status}")

        return lines
