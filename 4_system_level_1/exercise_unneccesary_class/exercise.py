from datetime import date
from typing import Iterable


class AvailabilityChecker:
    def is_available(
        self,
        booked_dates: Iterable[date],
        requested_date: date,
    ) -> bool:
        return requested_date not in booked_dates

    def available_dates(
        self,
        booked_dates: Iterable[date],
        requested_dates: Iterable[date],
    ) -> list[date]:
        return [day for day in requested_dates if self.is_available(booked_dates, day)]


def main() -> None:
    booked_dates = {
        date(2026, 8, 3),
        date(2026, 8, 5),
        date(2026, 8, 7),
    }

    requested_dates = [
        date(2026, 8, 2),
        date(2026, 8, 3),
        date(2026, 8, 4),
        date(2026, 8, 5),
        date(2026, 8, 6),
    ]

    checker = AvailabilityChecker()

    print("Availability")
    print("------------")

    for day in requested_dates:
        status = "Available" if checker.is_available(booked_dates, day) else "Booked"
        print(f"{day}: {status}")

    print()
    print("Available dates:")
    for day in checker.available_dates(
        booked_dates,
        requested_dates,
    ):
        print(f"- {day}")


if __name__ == "__main__":
    main()
