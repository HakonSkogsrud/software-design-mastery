from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Booking:
    booking_id: str
    guest_name: str
    room_type: str
    check_in: date
    check_out: date
    guest_count: int
    status: str
    total_price: Decimal
