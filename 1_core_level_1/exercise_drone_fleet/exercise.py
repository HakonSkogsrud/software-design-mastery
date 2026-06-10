def schedule_battery_replacement(drone):
    if (
        drone["hardware"]["battery"]["health"] < 70
        and drone["hardware"]["battery"]["cycles"] > 500
        and drone["mission"]["status"] == "idle"
    ):
        print(f"Schedule replacement for drone {drone['id']}")


def main():
    drones = [
        {
            "id": "drone_1",
            "hardware": {
                "battery": {"health": 65, "cycles": 600},
                "motors": {"status": "good"},
            },
            "mission": {"status": "idle"},
        },
        {
            "id": "drone_2",
            "hardware": {
                "battery": {"health": 80, "cycles": 300},
                "motors": {"status": "good"},
            },
            "mission": {"status": "active"},
        },
    ]

    for drone in drones:
        schedule_battery_replacement(drone)


if __name__ == "__main__":
    main()
