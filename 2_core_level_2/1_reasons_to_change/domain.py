from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Room:
    number: int
    room_type: str
    price_per_night: Decimal
    available: bool = True

    def is_available(self) -> bool:
        return self.available

    def mark_available(self) -> None:
        self.available = True

    def mark_unavailable(self) -> None:
        self.available = False


@dataclass
class Booking:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    total_price: Decimal
    status: BookingStatus = BookingStatus.CONFIRMED
    is_corporate: bool = False
    requires_invoice: bool = False

    def is_confirmed(self) -> bool:
        return self.status is BookingStatus.CONFIRMED

    def cancel(self) -> None:
        self.status = BookingStatus.CANCELLED

    def move_to_room(self, new_room_number: int, new_total_price: Decimal) -> None:
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
