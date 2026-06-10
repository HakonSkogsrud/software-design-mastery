class EquipmentRental:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []

    def add_item(self, equipment_id, category, days, daily_rate, insured=False):
        item = {
            "equipment_id": equipment_id,
            "category": category,
            "days": days,
            "daily_rate": daily_rate,
            "insured": insured,
        }
        self.items.append(item)

    def calculate_total(self, price_adjusters, include_insurance):
        total = 0

        for item in self.items:
            subtotal = item["days"] * item["daily_rate"]

            if include_insurance and item["insured"]:
                subtotal += item["days"] * 5.00

            for adjuster in price_adjusters:
                subtotal = adjuster(item, subtotal)

            total += subtotal

        return total


def weekend_discount(item, subtotal):
    if item["days"] >= 3:
        return subtotal * 0.9

    return subtotal


def heavy_equipment_surcharge(item, subtotal):
    if item["category"] == "heavy":
        return subtotal + 25.00

    return subtotal


def main() -> None:
    rental = EquipmentRental("Maya")

    rental.add_item(101, "camera", 3, 25.00, insured=True)
    rental.add_item(205, "heavy", 1, 120.00)
    rental.add_item(318, "audio", 5, 15.50, insured=True)

    total_price = rental.calculate_total(
        price_adjusters=[
            weekend_discount,
            heavy_equipment_surcharge,
        ],
        include_insurance=True,
    )

    print(total_price)


if __name__ == "__main__":
    main()
