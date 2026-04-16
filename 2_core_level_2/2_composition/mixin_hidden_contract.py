class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class RetryMixin:
    def retry_count(self):
        return self.max_retries  # hidden dependency


class NotificationService(LoggingMixin, RetryMixin):
    def __init__(self):
        self.max_retries = 3  # must remember this!

    def send_confirmation(self, email):
        self.log(f"Sending confirmation with up to {self.retry_count()} retries")
        print(f"Email sent to {email}")


def main():
    service = NotificationService()
    service.send_confirmation("alice@example.com")


if __name__ == "__main__":
    main()
