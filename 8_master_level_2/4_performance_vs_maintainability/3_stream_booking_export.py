from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class Booking:
    reference: str
    customer_name: str
    check_in: date
    total_price: Decimal


@dataclass(frozen=True)
class BookingExport:
    reference: str
    customer_name: str
    check_in: str
    total_price: str

    @classmethod
    def from_booking(cls, booking: Booking) -> "BookingExport":
        return cls(
            reference=booking.reference,
            customer_name=booking.customer_name,
            check_in=booking.check_in.isoformat(),
            total_price=str(booking.total_price),
        )


class BookingRepository:
    def iter_all(self) -> Iterator[Booking]:
        for index in range(1, 1_000_001):
            yield Booking(
                reference=f"BKG-{index:07}",
                customer_name=f"Customer {index}",
                check_in=date(2026, 8, 1) + timedelta(days=index % 30),
                total_price=Decimal("250.00"),
            )


def export_bookings(
    repository: BookingRepository,
) -> Iterator[BookingExport]:
    for booking in repository.iter_all():
        yield BookingExport.from_booking(booking)


def main() -> None:
    repository = BookingRepository()

    exported_bookings = export_bookings(repository)

    # The export is consumed incrementally. It is never stored
    # as one list containing a million records.
    for index, booking in enumerate(exported_bookings):
        print(booking)

        # Keep the demonstration output manageable.
        if index == 4:
            break


if __name__ == "__main__":
    main()
