from dataclasses import dataclass
from enum import StrEnum


class MissionStatus(StrEnum):
    IDLE = "idle"
    ACTIVE = "active"


@dataclass(frozen=True)
class Battery:
    health: int
    cycles: int

    def needs_replacement(self) -> bool:
        return self.health < 70 and self.cycles > 500


@dataclass(frozen=True)
class Motors:
    status: str


@dataclass(frozen=True)
class Hardware:
    battery: Battery
    motors: Motors


@dataclass(frozen=True)
class Mission:
    status: MissionStatus

    def is_idle(self) -> bool:
        return self.status is MissionStatus.IDLE


@dataclass(frozen=True)
class Drone:
    id: str
    hardware: Hardware
    mission: Mission

    def can_schedule_battery_replacement(self) -> bool:
        return self.hardware.battery.needs_replacement() and self.mission.is_idle()


def schedule_battery_replacement(drone: Drone) -> None:
    if drone.can_schedule_battery_replacement():
        print(f"Schedule replacement for drone {drone.id}")


def main() -> None:
    drones = [
        Drone(
            id="drone_1",
            hardware=Hardware(
                battery=Battery(health=65, cycles=600),
                motors=Motors(status="good"),
            ),
            mission=Mission(status=MissionStatus.IDLE),
        ),
        Drone(
            id="drone_2",
            hardware=Hardware(
                battery=Battery(health=80, cycles=300),
                motors=Motors(status="good"),
            ),
            mission=Mission(status=MissionStatus.ACTIVE),
        ),
    ]

    for drone in drones:
        schedule_battery_replacement(drone)


if __name__ == "__main__":
    main()
