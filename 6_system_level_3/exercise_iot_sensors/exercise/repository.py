import asyncio

from models import SensorReading


class InMemoryAsyncReadingRepository:
    def __init__(self) -> None:
        self.readings: list[SensorReading] = []

    async def save(
        self,
        reading: SensorReading,
    ) -> None:
        await asyncio.sleep(0.05)
        self.readings.append(reading)
