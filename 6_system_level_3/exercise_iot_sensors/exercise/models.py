from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float
    recorded_at: datetime
    is_anomalous: bool = False

    def mark_as_anomalous(self) -> None:
        self.is_anomalous = True
