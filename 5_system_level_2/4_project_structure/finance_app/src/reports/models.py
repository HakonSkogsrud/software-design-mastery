from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SpendingReport:
    total_spent: Decimal
    totals_by_category: dict[str, Decimal]
    transaction_count: int
