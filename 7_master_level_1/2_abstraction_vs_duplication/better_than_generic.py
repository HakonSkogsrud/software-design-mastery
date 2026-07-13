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


def generate_transfer_receipt(transfer: Transfer) -> str:
    return "\n".join(
        [
            "Transfer receipt",
            f"Reference: {transfer.reference}",
            f"Amount: EUR {transfer.amount:.2f}",
            f"Settlement date: {transfer.settlement_date}",
        ]
    )


def generate_invoice(invoice: Invoice) -> str:
    return "\n".join(
        [
            "Invoice",
            f"Invoice number: {invoice.invoice_number}",
            f"Amount: EUR {invoice.amount:.2f}",
            f"VAT: EUR {invoice.vat_amount:.2f}",
            f"Due date: {invoice.due_date}",
            "Payment is subject to the applicable terms and conditions.",
        ]
    )


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

    print(generate_transfer_receipt(transfer))
    print()
    print(generate_invoice(invoice))


if __name__ == "__main__":
    main()
