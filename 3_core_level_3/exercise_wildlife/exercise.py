from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class MissionStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Mission:
    mission_id: str
    species: str
    tracking_days: int
    tracker_id: str
    estimated_cost: Decimal
    status: MissionStatus


def main() -> None:
    mission = Mission(
        mission_id="M-001",
        species="Snow Leopard",
        tracking_days=14,
        tracker_id="TRK-17",
        estimated_cost=Decimal("2800.00"),
        status=MissionStatus.ACTIVE,
    )

    mission.tracker_id = "TRK-99"
    mission.estimated_cost = Decimal("0.00")
    mission.status = MissionStatus.COMPLETED

    print(mission)


if __name__ == "__main__":
    main()
