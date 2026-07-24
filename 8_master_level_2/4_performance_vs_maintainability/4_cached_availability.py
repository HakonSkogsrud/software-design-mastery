from dataclasses import dataclass
from datetime import date, time
from typing import Protocol


@dataclass(frozen=True)
class RoomId:
    value: str


@dataclass(frozen=True)
class TimeSlot:
    starts_at: time
    ends_at: time


@dataclass(frozen=True)
class Availability:
    room_id: RoomId
    day: date
    available_slots: tuple[TimeSlot, ...]


class AvailabilityService(Protocol):
    def get_availability(
        self,
        room_id: RoomId,
        day: date,
    ) -> Availability: ...


class AvailabilityCache(Protocol):
    def get(
        self,
        room_id: RoomId,
        day: date,
    ) -> Availability | None: ...

    def set(
        self,
        room_id: RoomId,
        day: date,
        availability: Availability,
    ) -> None: ...

    def invalidate(
        self,
        room_id: RoomId,
        day: date,
    ) -> None: ...


class CalculatedAvailabilityService:
    def get_availability(
        self,
        room_id: RoomId,
        day: date,
    ) -> Availability:
        print("Calculating availability...")

        return Availability(
            room_id=room_id,
            day=day,
            available_slots=(
                TimeSlot(
                    starts_at=time(9, 0),
                    ends_at=time(10, 0),
                ),
                TimeSlot(
                    starts_at=time(10, 0),
                    ends_at=time(11, 0),
                ),
            ),
        )


class InMemoryAvailabilityCache:
    def __init__(self) -> None:
        self._entries: dict[
            tuple[RoomId, date],
            Availability,
        ] = {}

    def get(
        self,
        room_id: RoomId,
        day: date,
    ) -> Availability | None:
        return self._entries.get((room_id, day))

    def set(
        self,
        room_id: RoomId,
        day: date,
        availability: Availability,
    ) -> None:
        self._entries[(room_id, day)] = availability

    def invalidate(
        self,
        room_id: RoomId,
        day: date,
    ) -> None:
        self._entries.pop((room_id, day), None)


class CachedAvailabilityService:
    def __init__(
        self,
        service: AvailabilityService,
        cache: AvailabilityCache,
    ) -> None:
        self._service = service
        self._cache = cache

    def get_availability(
        self,
        room_id: RoomId,
        day: date,
    ) -> Availability:
        cached = self._cache.get(room_id, day)

        if cached is not None:
            print("Using cached availability...")
            return cached

        availability = self._service.get_availability(
            room_id,
            day,
        )
        self._cache.set(room_id, day, availability)

        return availability


def main() -> None:
    cache = InMemoryAvailabilityCache()
    service = CachedAvailabilityService(
        service=CalculatedAvailabilityService(),
        cache=cache,
    )

    room_id = RoomId("ROOM-101")
    booking_day = date(2026, 8, 10)

    service.get_availability(room_id, booking_day)
    service.get_availability(room_id, booking_day)

    print("A booking was created. Invalidating the cache...")
    cache.invalidate(room_id, booking_day)

    service.get_availability(room_id, booking_day)


if __name__ == "__main__":
    main()
