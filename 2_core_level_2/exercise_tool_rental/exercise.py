from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Equipment:
    id: str
    name: str
    daily_rate: Decimal
    available: bool = True


@dataclass
class RentalRequest:
    customer_name: str
    customer_email: str
    equipment_id: str
    rental_days: int
    loyalty_tier: str = "standard"
    include_insurance: bool = False
    send_confirmation: bool = True
    preferred_channel: str = "email"


class PricingService:
    def calculate_price(
        self,
        equipment: Equipment,
        rental_request: RentalRequest,
    ) -> Decimal:
        total = equipment.daily_rate * rental_request.rental_days

        if rental_request.loyalty_tier == "gold":
            total *= Decimal("0.90")

        if rental_request.include_insurance:
            total += Decimal("15.00") * rental_request.rental_days

        return total


def main() -> None:
    equipment = Equipment(
        id="CAM-01",
        name="Cinema Camera",
        daily_rate=Decimal("120.00"),
    )

    request = RentalRequest(
        customer_name="Alice",
        customer_email="alice@example.com",
        equipment_id="CAM-01",
        rental_days=3,
        loyalty_tier="gold",
        include_insurance=True,
        preferred_channel="email",
    )

    pricing = PricingService()
    total = pricing.calculate_price(equipment, request)

    print(f"Total price: {total}")


if __name__ == "__main__":
    main()
