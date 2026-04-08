from datetime import date

from adapters.in_memory_booking_repository import InMemoryBookingRepository
from adapters.standard_pricing_policy import StandardPricingPolicy
from application.booking_service import BookingService


def main() -> None:
    booking_repository = InMemoryBookingRepository()
    pricing_policy = StandardPricingPolicy()
    booking_service = BookingService(
        booking_repository=booking_repository,
        pricing_policy=pricing_policy,
    )

    booking = booking_service.create_booking(
        guest_name="Alice Johnson",
        room_type="double",
        check_in=date(2026, 5, 10),
        check_out=date(2026, 5, 14),
        guest_count=2,
    )

    print("Created booking:")
    print(booking)

    booking_service.confirm_booking(booking.booking_id)

    confirmed_booking = booking_repository.get(booking.booking_id)
    print()
    print("Confirmed booking:")
    print(confirmed_booking)


if __name__ == "__main__":
    main()
