from dataclasses import dataclass


class FinanceError(Exception):
    pass


@dataclass(frozen=True)
class NoTransactionsForPeriodError(FinanceError):
    message: str
    month: int
    year: int

    def __str__(self) -> str:
        return f"{self.message} (year={self.year}, month={self.month})"
