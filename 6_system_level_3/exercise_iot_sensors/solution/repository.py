import asyncio

from models import SensorReading


class AsyncReadingDatabase:
    def __init__(self) -> None:
        self.readings: list[SensorReading] = []

    async def save(self, reading: SensorReading) -> None:
        await asyncio.sleep(0.05)
        self.readings.append(reading)


class SyncReadingRepository:
    def __init__(self, database: AsyncReadingDatabase) -> None:
        self._database = database

    def save(self, reading: SensorReading) -> None:
        asyncio.run(self._database.save(reading))

    @property
    def readings(self) -> list[SensorReading]:
        return list(self._database.readings)
