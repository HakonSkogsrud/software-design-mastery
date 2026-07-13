from typing import Protocol

from models import SensorReading


class AsyncSensorClient(Protocol):
    async def receive_reading(self) -> SensorReading: ...


class AsyncReadingRepository(Protocol):
    async def save(self, reading: SensorReading) -> None: ...
