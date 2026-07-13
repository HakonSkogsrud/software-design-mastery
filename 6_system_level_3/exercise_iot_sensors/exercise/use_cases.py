from ports import (
    AsyncReadingRepository,
    AsyncSensorClient,
)

MIN_TEMPERATURE = -20.0
MAX_TEMPERATURE = 50.0


async def process_reading(
    sensor_client: AsyncSensorClient,
    repository: AsyncReadingRepository,
) -> None:
    reading = await sensor_client.receive_reading()

    if reading.temperature < MIN_TEMPERATURE or reading.temperature > MAX_TEMPERATURE:
        reading.mark_as_anomalous()

    await repository.save(reading)
