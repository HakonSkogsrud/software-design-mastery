from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # No default: the application refuses to start unless this is provided.
    database_url: str
    log_level: str = "INFO"


def main() -> None:
    settings = Settings()
    print(f"Using database: {settings.database_url}")


if __name__ == "__main__":
    main()
