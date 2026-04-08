from datetime import date
from decimal import Decimal
from typing import Protocol


class PricingPolicy(Protocol):
    def calculate_price(
        self,
        room_type: str,
        check_in: date,
        check_out: date,
        guest_count: int,
    ) -> Decimal: ...
