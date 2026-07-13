from models import SensorReading
from ports import ReadingRepository

MIN_TEMPERATURE = -20.0
MAX_TEMPERATURE = 50.0


def process_reading(
    reading: SensorReading,
    repository: ReadingRepository,
) -> None:
    if reading.temperature < MIN_TEMPERATURE or reading.temperature > MAX_TEMPERATURE:
        reading.mark_as_anomalous()

    repository.save(reading)
