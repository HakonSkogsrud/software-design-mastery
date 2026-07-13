import asyncio

from mqtt_client import FakeMqttSensorClient
from repository import AsyncReadingDatabase, SyncReadingRepository
from use_cases import process_reading


def main() -> None:
    sensor_client = FakeMqttSensorClient()
    database = AsyncReadingDatabase()
    repository = SyncReadingRepository(database)

    for _ in range(2):
        reading = asyncio.run(sensor_client.receive_reading())
        process_reading(reading, repository)

    print("Stored readings:")

    for reading in repository.readings:
        status = "anomalous" if reading.is_anomalous else "normal"

        print(f"- {reading.sensor_id}: {reading.temperature}°C ({status})")


if __name__ == "__main__":
    main()
