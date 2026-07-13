from enum import StrEnum

from pydantic_settings import BaseSettings


class PaymentProvider(StrEnum):
    STRIPE = "stripe"
    ADYEN = "adyen"


class Settings(BaseSettings):
    payment_provider: PaymentProvider

    stripe_api_key: str | None = None

    adyen_client_id: str | None = None
    adyen_client_secret: str | None = None


def main() -> None:
    settings = Settings()

    if settings.payment_provider == PaymentProvider.STRIPE:
        print(f"Using Stripe key: {settings.stripe_api_key}")

    if settings.payment_provider == PaymentProvider.ADYEN:
        print(f"Using Adyen client: {settings.adyen_client_id}")


if __name__ == "__main__":
    main()
