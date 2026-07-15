from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Artifact(StrEnum):
    PAINTING = "painting"
    MANUSCRIPT = "manuscript"
    SCULPTURE = "sculpture"
    TEXTILE = "textile"


@dataclass
class Artwork:
    type: Artifact
    max_humidity: int | None = None
    max_temperature: int | None = None
    max_vibration: int | None = None
    max_exposure: int | None = None


class PreservationPolicy(Protocol):
    def check(self, current: int, artwork: Artwork) -> None: ...


class HumidityPolicy:
    def check(self, current: int, artwork: Artwork) -> None:
        if artwork.max_humidity is not None and current > artwork.max_humidity:
            print("Humidity too high")


class TemperaturePolicy:
    def check(self, current: int, artwork: Artwork) -> None:
        if artwork.max_temperature is not None and current > artwork.max_temperature:
            print("Temperature too high")


class VibrationPolicy:
    def check(self, current: int, artwork: Artwork) -> None:
        if artwork.max_vibration is not None and current > artwork.max_vibration:
            print("Vibration too high")


class ExposurePolicy:
    def check(self, current: int, artwork: Artwork) -> None:
        if artwork.max_exposure is not None and current > artwork.max_exposure:
            print("Light exposure too high")


class ArtworkPreservationService:
    def __init__(self, id: str) -> None:
        self.id = id
        self.artworks: list[Artwork] = []

        self.policies: list[PreservationPolicy] = [
            HumidityPolicy(),
            TemperaturePolicy(),
            VibrationPolicy(),
            ExposurePolicy(),
        ]

    def add_artwork(self, artwork: Artwork) -> None:
        self.artworks.append(artwork)

    def inspect(
        self,
        current_humidity: int,
        current_temperature: int,
        current_vibration: int,
        current_exposure: int,
    ) -> None:
        current_values = [
            current_humidity,
            current_temperature,
            current_vibration,
            current_exposure,
        ]

        for artwork in self.artworks:
            print(f"Inspecting {artwork.type}...")

            for policy, current in zip(
                self.policies,
                current_values,
                strict=True,
            ):
                policy.check(current, artwork)


def main() -> None:
    preservation_service = ArtworkPreservationService(id="P-101")

    preservation_service.add_artwork(
        Artwork(
            type=Artifact.PAINTING,
            max_humidity=50,
            max_temperature=21,
        )
    )
    preservation_service.add_artwork(
        Artwork(
            type=Artifact.MANUSCRIPT,
            max_humidity=40,
        )
    )
    preservation_service.add_artwork(
        Artwork(
            type=Artifact.SCULPTURE,
            max_vibration=5,
        )
    )
    preservation_service.add_artwork(
        Artwork(
            type=Artifact.TEXTILE,
            max_humidity=35,
            max_exposure=45,
        )
    )

    preservation_service.inspect(
        current_humidity=55,
        current_temperature=22,
        current_vibration=6,
        current_exposure=50,
    )


if __name__ == "__main__":
    main()
