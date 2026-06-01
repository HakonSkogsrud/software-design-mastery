from decimal import Decimal
from functools import partial


def convert_currency(
    amount: Decimal,
    source_currency: str,
    rates: dict[str, Decimal],
    target_currency: str,
) -> Decimal:
    source_rate = rates[source_currency]
    target_rate = rates[target_currency]

    eur_amount = amount / source_rate

    return eur_amount * target_rate


def create_currency_converter(
    rates: dict[str, Decimal],
    target_currency: str,
):
    def convert(
        amount: Decimal,
        source_currency: str,
    ) -> Decimal:
        source_rate = rates[source_currency]
        target_rate = rates[target_currency]

        eur_amount = amount / source_rate

        return eur_amount * target_rate

    return convert


def main() -> None:
    rates = {
        "EUR": Decimal("1.0"),
        "USD": Decimal("1.08"),
        "GBP": Decimal("0.85"),
    }

    eur_converter = partial(
        convert_currency,
        rates=rates,
        target_currency="EUR",
    )

    eur_converter_closure = create_currency_converter(
        rates=rates,
        target_currency="EUR",
    )

    print(eur_converter(Decimal("100"), "USD"))
    print(eur_converter(Decimal("50"), "GBP"))
    print(eur_converter(Decimal("200"), "USD"))

    print(eur_converter_closure(Decimal("100"), "USD"))
    print(eur_converter_closure(Decimal("50"), "GBP"))
    print(eur_converter_closure(Decimal("200"), "USD"))


if __name__ == "__main__":
    main()
