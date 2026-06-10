from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RestorationJob:
    catalog_number: str
    title: str
    humidity_percent: int
    fragile_page_count: int
    estimated_cost: Decimal
    handling_level: str
    status: str


def validate_catalog_number(catalog_number: str) -> None:
    if not catalog_number.startswith("RB-"):
        raise ValueError("Catalog number must start with RB-")


def calculate_restoration_quote(
    fragile_page_count: int,
    handling_level: str,
) -> Decimal:
    base = Decimal("150.00")
    per_page = Decimal("8.00") * fragile_page_count

    if handling_level == "restricted":
        return base + per_page + Decimal("120.00")

    if handling_level == "standard":
        return base + per_page

    return base + per_page


class RestorationService:
    def create_job(
        self,
        catalog_number: str,
        title: str,
        humidity_percent: int,
        fragile_page_count: int,
        handling_level: str,
    ) -> RestorationJob:
        validate_catalog_number(catalog_number)

        if not title.strip():
            raise ValueError("Title cannot be empty")

        if fragile_page_count < 0:
            raise ValueError("Fragile page count cannot be negative")

        estimated_cost = calculate_restoration_quote(
            fragile_page_count=fragile_page_count,
            handling_level=handling_level,
        )

        return RestorationJob(
            catalog_number=catalog_number,
            title=title,
            humidity_percent=humidity_percent,
            fragile_page_count=fragile_page_count,
            estimated_cost=estimated_cost,
            handling_level=handling_level,
            status="intake",
        )

    def move_to_assessment(self, job: RestorationJob) -> None:
        if job.status != "intake":
            raise ValueError("Only intake jobs can move to assessment")

        if job.humidity_percent < 30 or job.humidity_percent > 55:
            raise ValueError("Humidity must be between 30 and 55 before assessment")

        job.status = "assessment"

    def start_restoration(self, job: RestorationJob) -> None:
        if job.status != "assessment":
            raise ValueError("Job must be in assessment first")

        if job.handling_level not in {"standard", "restricted"}:
            raise ValueError("Invalid handling level")

        job.status = "in_progress"

    def complete_job(self, job: RestorationJob) -> None:
        if job.status != "in_progress":
            raise ValueError("Only in-progress jobs can be completed")

        if job.estimated_cost < 0:
            raise ValueError("Estimated cost cannot be negative")

        job.status = "completed"


def print_job(job: RestorationJob) -> None:
    print(
        f"{job.catalog_number} | {job.title} | "
        f"humidity={job.humidity_percent}% | "
        f"fragile_pages={job.fragile_page_count} | "
        f"cost={job.estimated_cost} | "
        f"handling={job.handling_level} | "
        f"status={job.status}"
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
    service.move_to_assessment(job)
    print_job(job)

    service.start_restoration(job)
    print_job(job)

    service.complete_job(job)
    print_job(job)

    print("\nTrying to create an invalid job...")
    try:
        bad_job = RestorationJob(
            catalog_number="bad-number",
            title="",
            humidity_percent=10,
            fragile_page_count=-4,
            estimated_cost=Decimal("-50.00"),
            handling_level="unknown",
            status="whatever",
        )
        print_job(bad_job)
        raise ValueError("Invalid job was created directly")
    except ValueError as exc:
        print(f"Creation failed: {exc}")


if __name__ == "__main__":
    main()
