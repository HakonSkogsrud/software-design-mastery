from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from multiprocessing import Value


class MissionStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



@dataclass(frozen=True, slots=True)
class TrackingDays:
    value: int

    def __post_init__(self):
        if self.value < 1:
            raise ValueError("Tracking days must be atleast 1")

@dataclass(frozen=True, slots=True)
class TrackerId:
    value : str

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("tracker is cannot be empty")

@dataclass(frozen=True, slots=True)
class MissionId:
    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("mission id cannot be empty")

@dataclass(frozen=True, slots=True)
class Species:
    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("Species cannot be empty")

        
@dataclass
class Mission:
    mission_id: MissionId
    species: Species
    tracking_days: TrackingDays
    tracker_id: TrackerId
    _estimated_cost: Decimal
    status: MissionStatus

    @classmethod
    def create(cls,mission_id:str,
               species:str,
               tracking_days: int,
               tracker_id: str,
               estimated_cost):
        return Mission(
            mission_id=MissionId(mission_id),
            species=Species(species),
            tracking_days=TrackingDays(tracking_days),
            tracker_id = TrackerId(tracker_id),
            _estimated_cost=estimated_cost,
            status=MissionStatus.PLANNED
        )

    def active(self) -> None:
        if self.status != MissionStatus.PLANNED:
            raise ValueError("Only planned missions can be started")
        self.status = MissionStatus.ACTIVE

    def complete(self) -> None:
        if self.status != MissionStatus.ACTIVE:
            raise ValueError("Only active missions can be completed")
        self.status = MissionStatus.COMPLETED
        
    def cancel(self) -> None:
        if self.status not in [MissionStatus.PLANNED, MissionStatus.ACTIVE]:
            raise ValueError("only active or planned missions can be cancelled")
        self.status = MissionStatus.CANCELLED

    @property
    def estimated_cost(self) -> Decimal:
        return self._estimated_cost

    def update_tracker_id(self, new_id: str) -> None:
        if self.status != MissionStatus.PLANNED:
            raise ValueError("Can only change id of non-active missions")
        self.tracker_id = TrackerId(new_id)

    def update_estimated_cost(self, new_cost: Decimal) -> None:
        self._estimated_cost = Decimal(new_cost)

        
def main() -> None:

    mission = Mission.create(
        mission_id="M-001",
        species="Snow Leopard",
        tracking_days=14,
        tracker_id="TRK-17",
        estimated_cost=Decimal("2800.00"),
    )

    mission._estimated_cost = Decimal("0.00")
    mission.status = MissionStatus.COMPLETED

    print(mission)


if __name__ == "__main__":
    main()
