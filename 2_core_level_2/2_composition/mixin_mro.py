class ConsoleLoggingMixin:
    def log(self, message):
        print(f"[console] {message}")


class AuditLoggingMixin:
    def log(self, message):
        print(f"[audit] {message}")


class NotificationService(ConsoleLoggingMixin, AuditLoggingMixin):
    pass


def main():
    service = NotificationService()
    service.log("Sending confirmation")


if __name__ == "__main__":
    main()
