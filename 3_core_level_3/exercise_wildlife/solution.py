from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Self


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
    _tracker_id: str
    _estimated_cost: Decimal
    _status: MissionStatus

    def __post_init__(self) -> None:
        if not self.species.strip():
            raise ValueError("Species cannot be empty")

        if self.tracking_days < 1:
            raise ValueError("Tracking days must be at least 1")

        if not self._tracker_id.strip():
            raise ValueError("Tracker id cannot be empty")

        if self._estimated_cost < 0:
            raise ValueError("Estimated cost cannot be negative")

    @classmethod
    def create(
        cls,
        mission_id: str,
        species: str,
        tracking_days: int,
        tracker_id: str,
        estimated_cost: Decimal,
    ) -> Self:
        return cls(
            mission_id=mission_id,
            species=species,
            tracking_days=tracking_days,
            _tracker_id=tracker_id,
            _estimated_cost=estimated_cost,
            _status=MissionStatus.PLANNED,
        )

    @property
    def tracker_id(self) -> str:
        return self._tracker_id

    @property
    def estimated_cost(self) -> Decimal:
        return self._estimated_cost

    @property
    def status(self) -> MissionStatus:
        return self._status

    def assign_tracker(self, tracker_id: str) -> None:
        if self._status is not MissionStatus.PLANNED:
            raise ValueError("Tracker can only be changed before the mission starts")

        if not tracker_id.strip():
            raise ValueError("Tracker id cannot be empty")

        self._tracker_id = tracker_id

    def start(self) -> None:
        if self._status is not MissionStatus.PLANNED:
            raise ValueError("Only planned missions can be started")

        self._status = MissionStatus.ACTIVE

    def complete(self) -> None:
        if self._status is not MissionStatus.ACTIVE:
            raise ValueError("Only active missions can be completed")

        self._status = MissionStatus.COMPLETED

    def cancel(self) -> None:
        if self._status not in {
            MissionStatus.PLANNED,
            MissionStatus.ACTIVE,
        }:
            raise ValueError("Only planned or active missions can be cancelled")

        self._status = MissionStatus.CANCELLED


def main() -> None:
    mission = Mission.create(
        mission_id="M-001",
        species="Snow Leopard",
        tracking_days=14,
        tracker_id="TRK-17",
        estimated_cost=Decimal("2800.00"),
    )

    print("Created:", mission)

    mission.assign_tracker("TRK-99")
    print("After tracker change:", mission)

    mission.start()
    print("After start:", mission)

    mission.complete()
    print("After completion:", mission)

    print("Final status:", mission.status)
    print("Estimated cost:", mission.estimated_cost)


if __name__ == "__main__":
    main()
