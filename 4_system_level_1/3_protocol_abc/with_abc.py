import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int


class ReportExporter(ABC):
    def export_report(self, report: SpendingReport) -> None:
        self.validate_report(report)

        formatted_report = self.format_report(report)

        self.write_output(formatted_report)

    def validate_report(self, report: SpendingReport) -> None:
        if report.transaction_count == 0:
            raise ValueError("Cannot export an empty report")

    @abstractmethod
    def format_report(self, report: SpendingReport) -> str:
        pass

    @abstractmethod
    def write_output(self, formatted_report: str) -> None:
        pass


class CsvReportExporter(ReportExporter):
    def format_report(self, report: SpendingReport) -> str:
        lines = [
            "category,total",
            *[
                f"{category},{total}"
                for category, total in report.totals_by_category.items()
            ],
        ]

        return "\n".join(lines)

    def write_output(self, formatted_report: str) -> None:
        print("Writing CSV report")
        print(formatted_report)


class JsonReportExporter(ReportExporter):
    def format_report(self, report: SpendingReport) -> str:
        return json.dumps(
            {
                "total_spent": str(report.total_spent),
                "transaction_count": report.transaction_count,
                "totals_by_category": {
                    category: str(total)
                    for category, total in report.totals_by_category.items()
                },
            },
            indent=2,
        )

    def write_output(self, formatted_report: str) -> None:
        print("Writing JSON report")
        print(formatted_report)


def main() -> None:
    report = SpendingReport(
        total_spent=Decimal("112.34"),
        totals_by_category={
            "Food": Decimal("45.60"),
            "Transport": Decimal("12.75"),
            "Education": Decimal("53.99"),
        },
        transaction_count=5,
    )

    exporters: list[ReportExporter] = [
        CsvReportExporter(),
        JsonReportExporter(),
    ]

    for exporter in exporters:
        exporter.export_report(report)
        print()


if __name__ == "__main__":
    main()
