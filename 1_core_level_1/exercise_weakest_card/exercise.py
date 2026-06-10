def water_plant(
    plant_name,
    moisture_level,
    weather_forecast,
    notify_owner=True,
):
    water_amount = 0

    if moisture_level < 30:
        water_amount = 2

    if moisture_level < 15:
        water_amount = 4

    watering_event = {
        "plant_name": plant_name,
        "water_amount": water_amount,
        "moisture_level": moisture_level,
        "status": "completed",
    }

    watering_history.append(watering_event)

    print(f"Watered {plant_name} with {water_amount} liters")

    if notify_owner:
        print(f"Sending notification for {plant_name}")

    return watering_event


def main():
    global watering_history
    watering_history = []

    water_plant("Fern", 25, "sunny")
    water_plant("Cactus", 10, "cloudy", notify_owner=False)
    water_plant("Bamboo", 5, "rainy")


if __name__ == "__main__":
    main()
