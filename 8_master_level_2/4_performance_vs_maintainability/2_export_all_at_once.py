from dataclasses import dataclass
from datetime import date
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
    def find_all(self) -> list[Booking]:
        return [
            Booking(
                reference="BKG-1001",
                customer_name="Alice",
                check_in=date(2026, 8, 10),
                total_price=Decimal("250.00"),
            ),
            Booking(
                reference="BKG-1002",
                customer_name="Bob",
                check_in=date(2026, 8, 12),
                total_price=Decimal("180.00"),
            ),
            Booking(
                reference="BKG-1003",
                customer_name="Charlie",
                check_in=date(2026, 8, 15),
                total_price=Decimal("320.00"),
            ),
        ]


def export_bookings(
    repository: BookingRepository,
) -> list[BookingExport]:
    return [BookingExport.from_booking(booking) for booking in repository.find_all()]


def main() -> None:
    repository = BookingRepository()
    exported_bookings = export_bookings(repository)

    for booking in exported_bookings:
        print(booking)


if __name__ == "__main__":
    main()
