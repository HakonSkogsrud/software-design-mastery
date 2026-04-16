class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class RetryMixin:
    def retry_count(self):
        return 3


class NotificationService(LoggingMixin, RetryMixin):
    def send_confirmation(self, email):
        self.log(f"Sending confirmation with up to {self.retry_count()} retries")
        print(f"Email sent to {email}")


def main():
    service = NotificationService()
    service.send_confirmation("alice@example.com")


if __name__ == "__main__":
    main()
