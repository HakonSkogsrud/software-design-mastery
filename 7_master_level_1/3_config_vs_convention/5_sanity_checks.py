from enum import StrEnum

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Environment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class PaymentProvider(StrEnum):
    STRIPE = "stripe"
    ADYEN = "adyen"


class Settings(BaseSettings):
    environment: Environment
    database_url: str

    payment_provider: PaymentProvider

    stripe_api_key: str | None = None

    adyen_client_id: str | None = None
    adyen_client_secret: str | None = None

    @model_validator(mode="after")
    def validate_database_environment(self) -> "Settings":
        if (
            self.environment == Environment.PRODUCTION
            and "production" not in self.database_url
        ):
            raise ValueError("Production must use the production database.")

        return self

    @model_validator(mode="after")
    def validate_payment_provider(self) -> "Settings":
        if self.payment_provider == PaymentProvider.STRIPE:
            if not self.stripe_api_key:
                raise ValueError(
                    "STRIPE_API_KEY is required when PAYMENT_PROVIDER=stripe."
                )

        if self.payment_provider == PaymentProvider.ADYEN:
            if not self.adyen_client_id or not self.adyen_client_secret:
                raise ValueError(
                    "ADYEN_CLIENT_ID and ADYEN_CLIENT_SECRET are required "
                    "when PAYMENT_PROVIDER=adyen."
                )

        return self


def main() -> None:
    settings = Settings()
    print("Configuration is valid.")
    print(settings)


if __name__ == "__main__":
    main()
