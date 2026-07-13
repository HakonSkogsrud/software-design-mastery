from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Dangerous: production might silently fall back to a local or wrong database.
    database_url: str = "postgres://localhost/booking"
    log_level: str = "INFO"


def main() -> None:
    settings = Settings()
    print(f"Using database: {settings.database_url}")


if __name__ == "__main__":
    main()
