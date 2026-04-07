from domain import Booking


class RetryMixin:
    def retry_count(self) -> int:
        return 3


class EmailNotificationMixin:
    def send_email(self, booking: Booking) -> None:
        print(
            f"[EMAIL] Sent confirmation to {booking.guest_email} "
            f"for room {booking.room_number}"
        )


class SMSNotificationMixin:
    def send_sms(self, booking: Booking) -> None:
        print(
            f"[SMS] Sent confirmation to {booking.guest_email} "
            f"for room {booking.room_number}"
        )


class BookingNotifier(RetryMixin, EmailNotificationMixin, SMSNotificationMixin):
    def send_confirmation(self, booking: Booking, channel: str) -> None:
        if channel == "sms":
            self.send_sms(booking)
        else:
            self.send_email(booking)

    def send_cancellation(self, booking: Booking, channel: str) -> None:
        if channel == "sms":
            print(
                f"[SMS] Sent cancellation to {booking.guest_email} "
                f"for room {booking.room_number}"
            )
        else:
            print(
                f"[EMAIL] Sent cancellation to {booking.guest_email} "
                f"for room {booking.room_number}"
            )
