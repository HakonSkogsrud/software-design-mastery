class UnsupportedCurrencyError(Exception):
    def __init__(self, currency: str) -> None:
        super().__init__(f"Unsupported currency: {currency}")


class SupportedCurrencyPolicy:
    def __init__(self, supported_currencies: set[str]) -> None:
        self._supported_currencies = supported_currencies

    def check(self, currency: str) -> None:
        if currency not in self._supported_currencies:
            raise UnsupportedCurrencyError(currency)
