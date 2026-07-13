import asyncio
from datetime import datetime

from models import SensorReading


class FakeMqttSensorClient:
    def __init__(self) -> None:
        self._readings = [
            SensorReading(
                sensor_id="sensor-001",
                temperature=21.5,
                humidity=45.0,
                recorded_at=datetime.now(),
            ),
            SensorReading(
                sensor_id="sensor-002",
                temperature=58.0,
                humidity=32.0,
                recorded_at=datetime.now(),
            ),
        ]

    async def receive_reading(self) -> SensorReading:
        await asyncio.sleep(0.2)

        if not self._readings:
            raise RuntimeError("No readings available")

        return self._readings.pop(0)
