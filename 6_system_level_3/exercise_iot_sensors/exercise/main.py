import asyncio

from mqtt_client import FakeMqttSensorClient
from repository import InMemoryAsyncReadingRepository
from use_cases import process_reading


async def main() -> None:
    sensor_client = FakeMqttSensorClient()
    repository = InMemoryAsyncReadingRepository()

    for _ in range(2):
        await process_reading(sensor_client, repository)

    print("Stored readings:")

    for reading in repository.readings:
        status = "anomalous" if reading.is_anomalous else "normal"

        print(f"- {reading.sensor_id}: {reading.temperature}°C ({status})")


if __name__ == "__main__":
    asyncio.run(main())
