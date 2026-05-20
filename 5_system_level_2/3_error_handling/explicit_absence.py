# explicit_absence.py

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Budget:
    category: str
    monthly_limit: Decimal


class BudgetRepository:
    def __init__(self) -> None:
        self._budgets = {
            "Food": Budget("Food", Decimal("500.00")),
            "Transport": Budget("Transport", Decimal("200.00")),
        }

    def find_by_category(self, category: str) -> Budget | None:
        return self._budgets.get(category)


def print_budget_status(
    category: str,
    spent: Decimal,
    budget_repository: BudgetRepository,
) -> None:
    budget = budget_repository.find_by_category(category)

    if budget is None:
        print(f"No budget configured for {category}")
        return

    remaining = budget.monthly_limit - spent

    print(f"{category}")
    print(f"Budget: €{budget.monthly_limit}")
    print(f"Spent: €{spent}")
    print(f"Remaining: €{remaining}")


def main() -> None:
    budget_repository = BudgetRepository()

    print_budget_status("Food", Decimal("125.00"), budget_repository)
    print()
    print_budget_status("Books", Decimal("80.00"), budget_repository)


if __name__ == "__main__":
    main()
