from decimal import Decimal


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


def main() -> None:
    rates = {
        "EUR": Decimal("1.0"),
        "USD": Decimal("1.08"),
        "GBP": Decimal("0.85"),
    }

    print(
        convert_currency(
            Decimal("100"),
            "USD",
            rates,
            "EUR",
        )
    )

    print(
        convert_currency(
            Decimal("50"),
            "GBP",
            rates,
            "EUR",
        )
    )

    print(
        convert_currency(
            Decimal("200"),
            "USD",
            rates,
            "EUR",
        )
    )


if __name__ == "__main__":
    main()
