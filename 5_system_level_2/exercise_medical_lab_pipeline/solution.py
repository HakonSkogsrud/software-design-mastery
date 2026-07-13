import csv
import logging
from datetime import date
from decimal import Decimal
from typing import Any, Protocol

from pydantic import BaseModel, ValidationError


class LabResultInput(BaseModel):
    patient_id: str
    test_name: str
    value: Decimal
    unit: str
    measured_on: date


class LabImportError(Exception):
    pass


class InvalidLabResultError(LabImportError):
    def __init__(
        self,
        hospital: str,
        file_path: str,
        line_number: int,
        errors: list[dict[str, Any]],
    ) -> None:
        self.hospital = hospital
        self.file_path = file_path
        self.line_number = line_number
        self.errors = errors

        super().__init__(
            f"Invalid lab result from {hospital} in {file_path} on line {line_number}"
        )


class Logger(Protocol):
    def info(self, msg: object, *args: object) -> None: ...

    def error(self, msg: object, *args: object) -> None: ...


class LabResultImporter(Protocol):
    def import_results(self) -> list[LabResultInput]: ...

    def hospital_name(self) -> str: ...


class NorthHospitalCsvImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_results(self) -> list[LabResultInput]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            return [
                self._parse_result(row, line_number)
                for line_number, row in enumerate(reader, start=2)
            ]

    def _parse_result(
        self,
        row: dict[str, str],
        line_number: int,
    ) -> LabResultInput:
        try:
            return LabResultInput.model_validate(
                {
                    "patient_id": row["patient_number"],
                    "test_name": row["test"],
                    "value": row["result"],
                    "unit": row["unit"],
                    "measured_on": row["date"],
                }
            )
        except ValidationError as error:
            raise InvalidLabResultError(
                hospital=self.hospital_name(),
                file_path=self.file_path,
                line_number=line_number,
                errors=error.errors(),
            ) from error

    def hospital_name(self) -> str:
        return "North Hospital"


class SouthHospitalCsvImporter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def import_results(self) -> list[LabResultInput]:
        with open(self.file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            return [
                self._parse_result(row, line_number)
                for line_number, row in enumerate(reader, start=2)
            ]

    def _parse_result(
        self,
        row: dict[str, str],
        line_number: int,
    ) -> LabResultInput:
        try:
            return LabResultInput.model_validate(
                {
                    "patient_id": row["patient_id"],
                    "test_name": row["analysis"],
                    "value": row["measured_value"],
                    "unit": row["measurement_unit"],
                    "measured_on": row["measured_at"],
                }
            )
        except ValidationError as error:
            raise InvalidLabResultError(
                hospital=self.hospital_name(),
                file_path=self.file_path,
                line_number=line_number,
                errors=error.errors(),
            ) from error

    def hospital_name(self) -> str:
        return "South Hospital"


class LabResultSynchronizer:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def synchronize(
        self,
        importer: LabResultImporter,
    ) -> list[LabResultInput]:
        self.logger.info(
            "Importing results from %s",
            importer.hospital_name(),
        )

        results = importer.import_results()

        self.logger.info(
            "Imported %s results from %s",
            len(results),
            importer.hospital_name(),
        )

        return results


def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("laboratory")


def log_validation_errors(
    logger: Logger,
    error: InvalidLabResultError,
) -> None:
    logger.error(
        "Import failed for %s in %s on line %s",
        error.hospital,
        error.file_path,
        error.line_number,
    )

    for validation_error in error.errors:
        location = ".".join(str(part) for part in validation_error["loc"])

        logger.error(
            "Field %s: %s; input=%r",
            location,
            validation_error["msg"],
            validation_error.get("input"),
        )


def print_results(results: list[LabResultInput]) -> None:
    for result in results:
        print(f"{result.patient_id}: {result.test_name} = {result.value} {result.unit}")


def main() -> None:
    logger = create_logger()

    importers: list[LabResultImporter] = [
        NorthHospitalCsvImporter("north_hospital_results.csv"),
        SouthHospitalCsvImporter("south_hospital_results.csv"),
    ]

    synchronizer = LabResultSynchronizer(logger)
    all_results: list[LabResultInput] = []

    for importer in importers:
        try:
            results = synchronizer.synchronize(importer)
        except InvalidLabResultError as error:
            log_validation_errors(logger, error)
            continue

        all_results.extend(results)

    print_results(all_results)


if __name__ == "__main__":
    main()
