from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    email_provider: str = "sendgrid"
    email_retry_count: int = 3
    log_level: str = "INFO"


def connect_to_database(settings: Settings) -> None:
    print(f"Connecting to database: {settings.database_url}")


def send_confirmation_email(to_email: str, settings: Settings) -> None:
    print(f"Sending email to {to_email}")
    print(f"Provider: {settings.email_provider}")
    print(f"Retries: {settings.email_retry_count}")


def main() -> None:
    settings = Settings()

    connect_to_database(settings)
    send_confirmation_email("guest@example.com", settings)


if __name__ == "__main__":
    main()
