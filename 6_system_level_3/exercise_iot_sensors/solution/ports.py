from typing import Protocol

from models import SensorReading


class ReadingRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
