from decimal import Decimal

from domain import Booking, BookingRequest, BookingStatus
from notifications import BookingNotifier
from pricing import calculate_total_price
from repository import InMemoryBookingRepository


class BookingService:
    def __init__(
        self,
        repository: InMemoryBookingRepository,
        notifier: BookingNotifier,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def create_booking(self, request: BookingRequest) -> Booking | None:
        room = self.repository.get_room(request.room_number)

        if room is None:
            print("Room does not exist")
            return None

        if request.nights <= 0:
            print("Invalid number of nights")
            return None

        if "@" not in request.guest_email:
            print("Invalid guest email")
            return None

        if not room.is_available():
            print("Room not available")
            return None

        if self.repository.active_booking_exists_for_room(room.number):
            print("Room already has an active booking")
            return None

        total_price = calculate_total_price(
            room=room,
            nights=request.nights,
            use_discount=request.use_discount,
        )

        if request.is_corporate:
            total_price *= Decimal("0.95")

        if request.requires_invoice and not request.is_corporate:
            total_price += Decimal("12.50")

        booking = Booking(
            guest_name=request.guest_name,
            guest_email=request.guest_email,
            room_number=request.room_number,
            nights=request.nights,
            total_price=total_price,
            status=BookingStatus.CONFIRMED,
            is_corporate=request.is_corporate,
            requires_invoice=request.requires_invoice,
        )

        self.repository.save_booking(booking)
        room.mark_unavailable()

        print(f"Booked room {room.number} for {request.guest_name}")

        if request.send_confirmation:
            if request.preferred_channel == "sms":
                self.notifier.send_confirmation(booking, "sms")
            else:
                self.notifier.send_confirmation(booking, "email")

        return booking

    def cancel_booking(
        self,
        guest_email: str,
        room_number: int,
        *,
        refund: bool = False,
        channel: str = "email",
    ) -> Booking | None:
        booking = self.repository.find_booking(guest_email, room_number)

        if booking is None:
            print("Booking not found")
            return None

        if not booking.is_confirmed():
            print("Booking already cancelled")
            return None

        room = self.repository.get_room(room_number)
        if room is None:
            print("Room does not exist")
            return None

        cancellation_fee = Decimal("0")
        if refund:
            if booking.nights < 2:
                cancellation_fee = Decimal("0")
            elif booking.is_corporate:
                cancellation_fee = Decimal("20")
            else:
                cancellation_fee = Decimal("35")

        booking.cancel()
        room.mark_available()

        print(f"Cancelled booking for room {room_number}")

        if refund:
            refund_amount = booking.total_price - cancellation_fee
            print(f"Refunding {refund_amount} to {guest_email}")

        self.notifier.send_cancellation(booking, channel)

        return booking

    def upgrade_room(
        self,
        guest_email: str,
        current_room_number: int,
        new_room_number: int,
    ) -> Booking | None:
        booking = self.repository.find_booking(guest_email, current_room_number)
        if booking is None:
            print("Booking not found")
            return None

        if not booking.is_confirmed():
            print("Only confirmed bookings can be upgraded")
            return None

        current_room = self.repository.get_room(current_room_number)
        new_room = self.repository.get_room(new_room_number)

        if current_room is None or new_room is None:
            print("Room does not exist")
            return None

        if not new_room.is_available():
            print("New room is not available")
            return None

        old_price = calculate_total_price(
            current_room,
            booking.nights,
            use_discount=False,
        )
        new_price = calculate_total_price(
            new_room,
            booking.nights,
            use_discount=False,
        )

        if booking.is_corporate:
            new_price *= Decimal("0.95")

        booking.move_to_room(new_room_number, new_price)
        current_room.mark_available()
        new_room.mark_unavailable()

        print(
            f"Upgraded booking for {guest_email} "
            f"from room {current_room_number} to {new_room_number}"
        )
        print(f"Additional charge: {new_price - old_price}")

        return booking
