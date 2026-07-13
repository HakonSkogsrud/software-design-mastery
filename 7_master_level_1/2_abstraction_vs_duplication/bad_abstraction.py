from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Transfer:
    reference: str
    amount: Decimal
    settlement_date: str


@dataclass(frozen=True)
class Invoice:
    invoice_number: str
    amount: Decimal
    vat_amount: Decimal
    due_date: str


def generate_document(
    title: str,
    reference: str,
    amount: Decimal,
    settlement_date: str | None = None,
    due_date: str | None = None,
    vat_amount: Decimal | None = None,
    include_legal_text: bool = False,
) -> str:
    lines = [
        title,
        f"Reference: {reference}",
        f"Amount: EUR {amount:.2f}",
    ]

    if settlement_date is not None:
        lines.append(f"Settlement date: {settlement_date}")

    if due_date is not None:
        lines.append(f"Due date: {due_date}")

    if vat_amount is not None:
        lines.append(f"VAT: EUR {vat_amount:.2f}")

    if include_legal_text:
        lines.append("Payment is subject to the applicable terms and conditions.")

    return "\n".join(lines)


def main() -> None:
    transfer = Transfer(
        reference="TR-2026-001",
        amount=Decimal("2500"),
        settlement_date="2026-07-10",
    )

    invoice = Invoice(
        invoice_number="INV-2026-001",
        amount=Decimal("2500"),
        vat_amount=Decimal("525"),
        due_date="2026-07-31",
    )

    print(
        generate_document(
            "Transfer receipt",
            transfer.reference,
            transfer.amount,
            settlement_date=transfer.settlement_date,
        )
    )

    print()

    print(
        generate_document(
            "Invoice",
            invoice.invoice_number,
            invoice.amount,
            due_date=invoice.due_date,
            vat_amount=invoice.vat_amount,
            include_legal_text=True,
        )
    )


if __name__ == "__main__":
    main()
