from typing import Protocol

from models import Transaction


class Report(Protocol):
    def generate(
        self,
        transactions: list[Transaction],
    ) -> object: ...


class MonthlySummaryReport:
    def generate(
        self,
        transactions: list[Transaction],
    ) -> object:
        print("Generating monthly summary...")


class ReportRegistry:
    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}

    def register(
        self,
        name: str,
        report: Report,
    ) -> None:
        self._reports[name] = report

    def get(
        self,
        name: str,
    ) -> Report:
        return self._reports[name]


class ReportEngine:
    def __init__(
        self,
        registry: ReportRegistry,
    ) -> None:
        self._registry = registry

    def generate(
        self,
        report_name: str,
        transactions: list[Transaction],
    ) -> object:
        report = self._registry.get(report_name)
        return report.generate(transactions)


def main() -> None:
    registry = ReportRegistry()
    registry.register(
        "monthly-summary",
        MonthlySummaryReport(),
    )

    engine = ReportEngine(registry)

    engine.generate(
        "monthly-summary",
        [],
    )


if __name__ == "__main__":
    main()
