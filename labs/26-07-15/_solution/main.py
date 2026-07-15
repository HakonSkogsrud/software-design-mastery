from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol


class Artifact(StrEnum):
    PAINTING = "painting"
    MANUSCRIPT = "manuscript"
    SCULPTURE = "sculpture"
    TEXTILE = "textile"


class LightSource(StrEnum):
    LED = "led"
    HALOGEN = "halogen"
    SUNLIGHT = "sunlight"


@dataclass(frozen=True)
class InspectionData:
    humidity: int
    temperature: int
    vibration: int
    exposure: int
    light_source: LightSource


@dataclass(frozen=True)
class Violation:
    message: str


class PreservationPolicy(Protocol):
    def check(self, data: InspectionData) -> Violation | None: ...


@dataclass(frozen=True)
class MaximumHumidity:
    maximum: int

    def check(self, data: InspectionData) -> Violation | None:
        if data.humidity > self.maximum:
            return Violation(
                f"humidity is too high: {data.humidity} exceeds {self.maximum}"
            )

        return None


@dataclass(frozen=True)
class MaximumTemperature:
    maximum: int

    def check(self, data: InspectionData) -> Violation | None:
        if data.temperature > self.maximum:
            return Violation(
                f"temperature is too high: {data.temperature} exceeds {self.maximum}"
            )

        return None


@dataclass(frozen=True)
class MaximumVibration:
    maximum: int

    def check(self, data: InspectionData) -> Violation | None:
        if data.vibration > self.maximum:
            return Violation(
                f"vibration is too high: {data.vibration} exceeds {self.maximum}"
            )

        return None


@dataclass(frozen=True)
class MaximumExposure:
    maximum: int

    def check(self, data: InspectionData) -> Violation | None:
        if data.exposure > self.maximum:
            return Violation(
                f"light exposure is too high: {data.exposure} exceeds {self.maximum}"
            )

        return None


@dataclass(frozen=True)
class AllowedLightSources:
    allowed: frozenset[LightSource]

    def check(self, data: InspectionData) -> Violation | None:
        if data.light_source not in self.allowed:
            return Violation(f"{data.light_source} light is not allowed")

        return None


@dataclass
class Artwork:
    type: Artifact
    policies: list[PreservationPolicy] = field(default_factory=list[PreservationPolicy])

    def inspect(self, data: InspectionData) -> list[Violation]:
        violations: list[Violation] = []

        for policy in self.policies:
            violation = policy.check(data)

            if violation is not None:
                violations.append(violation)

        return violations


class ArtworkPreservationService:
    def __init__(self, id: str) -> None:
        self.id = id
        self.artworks: list[Artwork] = []

    def add_artwork(self, artwork: Artwork) -> None:
        self.artworks.append(artwork)

    def inspect(self, data: InspectionData) -> None:
        for artwork in self.artworks:
            print(f"Inspecting {artwork.type}...")

            for violation in artwork.inspect(data):
                print(f"{artwork.type}: {violation.message}")


def main() -> None:
    preservation_service = ArtworkPreservationService(id="P-101")

    preservation_service.add_artwork(
        Artwork(
            type=Artifact.PAINTING,
            policies=[
                MaximumHumidity(50),
                MaximumTemperature(21),
                AllowedLightSources(frozenset({LightSource.LED})),
            ],
        )
    )

    preservation_service.add_artwork(
        Artwork(
            type=Artifact.MANUSCRIPT,
            policies=[
                MaximumHumidity(40),
                AllowedLightSources(frozenset({LightSource.LED})),
            ],
        )
    )

    preservation_service.add_artwork(
        Artwork(
            type=Artifact.SCULPTURE,
            policies=[
                MaximumVibration(5),
            ],
        )
    )

    preservation_service.add_artwork(
        Artwork(
            type=Artifact.TEXTILE,
            policies=[
                MaximumHumidity(35),
                MaximumExposure(45),
                AllowedLightSources(
                    frozenset(
                        {
                            LightSource.LED,
                            LightSource.HALOGEN,
                        }
                    )
                ),
            ],
        )
    )

    preservation_service.inspect(
        InspectionData(
            humidity=55,
            temperature=22,
            vibration=6,
            exposure=50,
            light_source=LightSource.SUNLIGHT,
        )
    )


if __name__ == "__main__":
    main()
