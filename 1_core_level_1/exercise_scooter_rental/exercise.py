scooters = [
    {"id": "SC-101", "hourly_rate": 8, "battery": 92},
    {"id": "SC-102", "hourly_rate": 12, "battery": 55},
]


def generate_customer_invoice(scooter_id, minutes):
    scooter = find_scooter(scooter_id)

    if scooter is None:
        return None

    total = scooter["hourly_rate"] * (minutes / 60)

    if minutes >= 300:
        total *= 0.85

    print(f"Invoice total: €{total:.2f}")

    return total


def estimate_maintenance_credit(scooter_id, usage_minutes):
    scooter = find_scooter(scooter_id)

    if scooter is None:
        return None

    credit = 0

    if usage_minutes >= 300:
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
    generate_customer_invoice("SC-101", 360)
    estimate_maintenance_credit("SC-102", 360)


if __name__ == "__main__":
    main()
