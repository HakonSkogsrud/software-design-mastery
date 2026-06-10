from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class RestorationStatus(StrEnum):
    INTAKE = "intake"
    ASSESSMENT = "assessment"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class CatalogNumber:
    value: str

    def __post_init__(self) -> None:
        if not self.value.startswith("RB-"):
            raise ValueError("Catalog number must start with RB-")


@dataclass(frozen=True, slots=True)
class HumidityPercent:
    value: int

    def __post_init__(self) -> None:
        if self.value < 30 or self.value > 55:
            raise ValueError("Humidity must be between 30 and 55")


@dataclass(frozen=True, slots=True)
class FragilePageCount:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Fragile page count cannot be negative")


@dataclass(frozen=True, slots=True)
class EstimatedCost:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Estimated cost cannot be negative")


class HandlingLevel(StrEnum):
    STANDARD = "standard"
    RESTRICTED = "restricted"


@dataclass
class RestorationJob:
    catalog_number: CatalogNumber
    title: str
    humidity_percent: HumidityPercent
    fragile_page_count: FragilePageCount
    estimated_cost: EstimatedCost
    handling_level: HandlingLevel
    status: RestorationStatus = RestorationStatus.INTAKE

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Title cannot be empty")

    def move_to_assessment(self) -> None:
        if self.status is not RestorationStatus.INTAKE:
            raise ValueError("Only intake jobs can move to assessment")
        self.status = RestorationStatus.ASSESSMENT

    def start_restoration(self) -> None:
        if self.status is not RestorationStatus.ASSESSMENT:
            raise ValueError("Job must be in assessment first")
        self.status = RestorationStatus.IN_PROGRESS

    def complete_job(self) -> None:
        if self.status is not RestorationStatus.IN_PROGRESS:
            raise ValueError("Only in-progress jobs can be completed")
        self.status = RestorationStatus.COMPLETED


def calculate_restoration_quote(
    fragile_page_count: FragilePageCount,
    handling_level: HandlingLevel,
) -> EstimatedCost:
    base = Decimal("150.00")
    per_page = Decimal("8.00") * fragile_page_count.value

    if handling_level is HandlingLevel.RESTRICTED:
        total = base + per_page + Decimal("120.00")
    else:
        total = base + per_page

    return EstimatedCost(total)


class RestorationService:
    def create_job(
        self,
        catalog_number: str,
        title: str,
        humidity_percent: int,
        fragile_page_count: int,
        handling_level: str,
    ) -> RestorationJob:
        validated_catalog_number = CatalogNumber(catalog_number)
        validated_humidity = HumidityPercent(humidity_percent)
        validated_page_count = FragilePageCount(fragile_page_count)
        validated_handling_level = HandlingLevel(handling_level)

        estimated_cost = calculate_restoration_quote(
            fragile_page_count=validated_page_count,
            handling_level=validated_handling_level,
        )

        return RestorationJob(
            catalog_number=validated_catalog_number,
            title=title,
            humidity_percent=validated_humidity,
            fragile_page_count=validated_page_count,
            estimated_cost=estimated_cost,
            handling_level=validated_handling_level,
            status=RestorationStatus.INTAKE,
        )


def print_job(job: RestorationJob) -> None:
    print(
        f"{job.catalog_number.value} | {job.title} | "
        f"humidity={job.humidity_percent.value}% | "
        f"fragile_pages={job.fragile_page_count.value} | "
        f"cost={job.estimated_cost.value} | "
        f"handling={job.handling_level.value} | "
        f"status={job.status.value}"
    )


def main() -> None:
    service = RestorationService()

    print("Creating a valid restoration job...")
    job = service.create_job(
        catalog_number="RB-1842",
        title="Bird Atlas of the Low Countries",
        humidity_percent=45,
        fragile_page_count=12,
        handling_level="restricted",
    )
    print_job(job)

    print("\nMoving through the workflow...")
    job.move_to_assessment()
    print_job(job)

    job.start_restoration()
    print_job(job)

    job.complete_job()
    print_job(job)

    print("\nTrying to create an invalid job...")
    try:
        bad_job = RestorationJob(
            catalog_number=CatalogNumber("bad-number"),
            title="",
            humidity_percent=HumidityPercent(10),
            fragile_page_count=FragilePageCount(-4),
            estimated_cost=EstimatedCost(Decimal("-50.00")),
            handling_level=HandlingLevel("unknown"),
            status=RestorationStatus.INTAKE,
        )
        print_job(bad_job)
        raise ValueError("Invalid job was created directly")
    except ValueError as exc:
        print(f"Creation failed: {exc}")


if __name__ == "__main__":
    main()
