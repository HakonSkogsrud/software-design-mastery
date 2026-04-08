from datetime import date
from decimal import Decimal

from ports.pricing_policy import PricingPolicy


class StandardPricingPolicy(PricingPolicy):
    def calculate_price(
        self,
        room_type: str,
        check_in: date,
        check_out: date,
        guest_count: int,
    ) -> Decimal:
        nights = (check_out - check_in).days

        base_prices = {
            "single": Decimal("90"),
            "double": Decimal("140"),
            "suite": Decimal("250"),
        }

        if room_type not in base_prices:
            raise ValueError(f"Unknown room type: {room_type}")

        total = base_prices[room_type] * nights

        if guest_count > 2:
            extra_guests = guest_count - 2
            total += Decimal("20") * extra_guests * nights

        if nights >= 3 and room_type in {"double", "suite"}:
            total *= Decimal("0.9")

        return total.quantize(Decimal("0.01"))
