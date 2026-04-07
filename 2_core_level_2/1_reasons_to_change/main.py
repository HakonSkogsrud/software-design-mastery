from booking_service import BookingService
from domain import BookingRequest
from notifications import BookingNotifier
from reporting import ReportingService
from repository import InMemoryBookingRepository


def main() -> None:
    repository = InMemoryBookingRepository()
    notifier = BookingNotifier()
    booking_service = BookingService(repository, notifier)
    reporting_service = ReportingService(repository)

    first_booking = booking_service.create_booking(
        BookingRequest(
            guest_name="Alice",
            guest_email="alice@example.com",
            room_number=201,
            nights=4,
            use_discount=True,
            send_confirmation=True,
            preferred_channel="email",
            is_corporate=False,
            requires_invoice=False,
        )
    )

    print(first_booking)
    print()

    second_booking = booking_service.create_booking(
        BookingRequest(
            guest_name="Bob",
            guest_email="bob@company.com",
            room_number=102,
            nights=2,
            use_discount=False,
            send_confirmation=True,
            preferred_channel="sms",
            is_corporate=True,
            requires_invoice=True,
        )
    )

    print(second_booking)
    print()

    booking_service.upgrade_room(
        guest_email="bob@company.com",
        current_room_number=102,
        new_room_number=301,
    )
    print()

    booking_service.cancel_booking(
        guest_email="alice@example.com",
        room_number=201,
        refund=True,
        channel="email",
    )
    print()

    print("Revenue (active only):", reporting_service.total_revenue())
    print(
        "Revenue (including cancelled):",
        reporting_service.total_revenue(include_cancelled=True),
    )
    print()

    for line in reporting_service.occupancy_report():
        print(line)


if __name__ == "__main__":
    main()
