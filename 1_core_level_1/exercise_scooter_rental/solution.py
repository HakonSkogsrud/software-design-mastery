scooters = [
    {"id": "SC-101", "hourly_rate": 8, "battery": 92},
    {"id": "SC-102", "hourly_rate": 12, "battery": 55},
]

LONG_RENTAL_MINUTES = 300


def is_long_rental(minutes):
    return minutes >= LONG_RENTAL_MINUTES


def generate_customer_invoice(scooter, minutes):
    total = scooter["hourly_rate"] * (minutes / 60)

    if is_long_rental(minutes):
        total *= 0.85

    print(f"Invoice total: €{total:.2f}")

    return total


def estimate_maintenance_credit(scooter, usage_minutes):
    credit = 0

    if is_long_rental(usage_minutes):
        credit += 10

    if scooter["battery"] < 60:
        credit += 5

    print(f"Maintenance credit: €{credit:.2f}")

    return credit


def find_scooter(scooter_id):
    for scooter in scooters:
        if scooter["id"] == scooter_id:
            return scooter

    return None


def main():
    scooter = find_scooter("SC-101")

    if scooter is not None:
        generate_customer_invoice(scooter, 360)

    scooter = find_scooter("SC-102")

    if scooter is not None:
        estimate_maintenance_credit(scooter, 360)


if __name__ == "__main__":
    main()
