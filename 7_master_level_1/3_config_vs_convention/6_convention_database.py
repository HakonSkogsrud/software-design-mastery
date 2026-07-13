from enum import StrEnum

from pydantic_settings import BaseSettings


class Environment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


DATABASES = {
    Environment.DEVELOPMENT: "postgres://localhost/booking",
    Environment.STAGING: "postgres://staging-db/booking",
    Environment.PRODUCTION: "postgres://production-db/booking",
}


class Settings(BaseSettings):
    environment: Environment


def get_database_url(settings: Settings) -> str:
    return DATABASES[settings.environment]


def main() -> None:
    settings = Settings()
    database_url = get_database_url(settings)

    print(f"Environment: {settings.environment}")
    print(f"Database: {database_url}")


if __name__ == "__main__":
    main()
