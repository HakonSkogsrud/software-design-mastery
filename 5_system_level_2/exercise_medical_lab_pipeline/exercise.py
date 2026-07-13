import csv
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class LabResult:
    patient_id: str
    test_name: str
    value: Decimal
    unit: str
    measured_on: date


class Logger(Protocol):
    def info(self, msg: object, *args: object) -> None: ...

    def error(self, msg: object, *args: object) -> None: ...


class LabResultImporter(Protocol):
    def import_results(self) -> list[LabResult]: ...

    def hospital_name(self) -> str: ...


class NorthHospitalCsvImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_results(self) -> list[LabResult]:
        results: list[LabResult] = []

        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try:
                    results.append(
                        LabResult(
                            patient_id=row["patient_number"],
                            test_name=row["test"],
                            value=Decimal(row["result"]),
                            unit=row["unit"],
                            measured_on=date.fromisoformat(row["date"]),
                        )
                    )
                except Exception:
                    pass

        return results

    def hospital_name(self) -> str:
        return "North Hospital"


class SouthHospitalCsvImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_results(self) -> list[LabResult]:
        results: list[LabResult] = []

        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try:
                    results.append(
                        LabResult(
                            patient_id=row["patient_id"],
                            test_name=row["analysis"],
                            value=Decimal(row["measured_value"]),
                            unit=row["measurement_unit"],
                            measured_on=date.fromisoformat(row["measured_at"]),
                        )
                    )
                except Exception:
                    continue

        return results

    def hospital_name(self) -> str:
        return "South Hospital"


class LabResultSynchronizer:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def synchronize(
        self,
        importer: LabResultImporter,
    ) -> list[LabResult]:
        self.logger.info(
            "Importing results from %s",
            importer.hospital_name(),
        )

        try:
            results = importer.import_results()
        except Exception:
            self.logger.error(
                "Could not import results from %s",
                importer.hospital_name(),
            )
            return []

        self.logger.info(
            "Imported %s results from %s",
            len(results),
            importer.hospital_name(),
        )

        return results


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("laboratory")


def print_results(results: list[LabResult]) -> None:
    for result in results:
        print(f"{result.patient_id}: {result.test_name} = {result.value} {result.unit}")


def main() -> None:
    logger = create_logger()

    importers: list[LabResultImporter] = [
        NorthHospitalCsvImporter("north_hospital_results.csv"),
        SouthHospitalCsvImporter("south_hospital_results.csv"),
    ]

    synchronizer = LabResultSynchronizer(logger)
    all_results: list[LabResult] = []

    for importer in importers:
        results = synchronizer.synchronize(importer)
        all_results.extend(results)

    print_results(all_results)


if __name__ == "__main__":
    main()
