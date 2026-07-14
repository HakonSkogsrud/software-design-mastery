from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

# -----------------------------
# Domain model
# -----------------------------


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    lines: list[OrderLine]

    @property
    def total(self) -> Decimal:
        return sum(
            (line.unit_price * line.quantity for line in self.lines),
            Decimal("0.00"),
        )


# -----------------------------
# Ports
# -----------------------------


class OrderRepository(Protocol):
    def add(self, order: Order) -> None: ...


class InventoryService(Protocol):
    def reserve(
        self,
        product_id: str,
        quantity: int,
    ) -> None: ...


# -----------------------------
# Additional workflows
# -----------------------------


def send_confirmation_email(order: Order) -> None:
    print(f"Sending confirmation email for order {order.id}")


def update_loyalty_points(order: Order) -> None:
    print(f"Updating loyalty points for customer {order.customer_id}")


def record_order_analytics(order: Order) -> None:
    print(f"Recording analytics for order {order.id}")


def send_partner_webhook(order: Order) -> None:
    print(f"Sending partner webhook for order {order.id}")


# -----------------------------
# Use case
# -----------------------------


def place_order(
    order: Order,
    repository: OrderRepository,
    inventory: InventoryService,
) -> None:
    for line in order.lines:
        inventory.reserve(
            product_id=line.product_id,
            quantity=line.quantity,
        )

    repository.add(order)

    send_confirmation_email(order)
    update_loyalty_points(order)
    record_order_analytics(order)
    send_partner_webhook(order)


# -----------------------------
# Adapters
# -----------------------------


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def add(self, order: Order) -> None:
        self._orders.append(order)

    def list_all(self) -> list[Order]:
        return list(self._orders)


class InMemoryInventoryService:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {
            "keyboard": 10,
            "mouse": 20,
        }

    def reserve(
        self,
        product_id: str,
        quantity: int,
    ) -> None:
        available = self._stock.get(product_id, 0)

        if available < quantity:
            raise ValueError(f"Insufficient stock for {product_id}")

        self._stock[product_id] = available - quantity


# -----------------------------
# Demo
# -----------------------------


def main() -> None:
    repository = InMemoryOrderRepository()
    inventory = InMemoryInventoryService()

    order = Order(
        id="order-001",
        customer_id="customer-123",
        lines=[
            OrderLine(
                product_id="keyboard",
                quantity=1,
                unit_price=Decimal("89.00"),
            ),
            OrderLine(
                product_id="mouse",
                quantity=2,
                unit_price=Decimal("35.00"),
            ),
        ],
    )

    place_order(
        order=order,
        repository=repository,
        inventory=inventory,
    )

    print(f"Placed order with total: €{order.total}")


if __name__ == "__main__":
    main()
