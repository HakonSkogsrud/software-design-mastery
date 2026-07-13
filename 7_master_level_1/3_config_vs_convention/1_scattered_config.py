import os


def connect_to_database() -> None:
    database_url = os.environ["DATABASE_URL"]
    print(f"Connecting to database: {database_url}")


def send_confirmation_email(to_email: str) -> None:
    provider = os.getenv("EMAIL_PROVIDER", "sendgrid")
    retry_count = int(os.getenv("EMAIL_RETRY_COUNT", "3"))

    print(f"Sending email to {to_email}")
    print(f"Provider: {provider}")
    print(f"Retries: {retry_count}")


def main() -> None:
    connect_to_database()
    send_confirmation_email("guest@example.com")


if __name__ == "__main__":
    main()
