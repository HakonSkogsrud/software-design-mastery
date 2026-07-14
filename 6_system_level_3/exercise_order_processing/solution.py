from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Callable, Protocol

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
# Domain events
# -----------------------------


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    customer_id: str
    total: Decimal
    occurred_at: datetime

    @classmethod
    def from_order(cls, order: Order) -> "OrderPlaced":
        return cls(
            order_id=order.id,
            customer_id=order.customer_id,
            total=order.total,
            occurred_at=datetime.now(UTC),
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


EventHandler = Callable[[object], None]


class EventBus(Protocol):
    def publish(self, event: object) -> None: ...

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None: ...


# -----------------------------
# Use case
# -----------------------------


def place_order(
    order: Order,
    repository: OrderRepository,
    inventory: InventoryService,
    event_bus: EventBus,
) -> None:
    for line in order.lines:
        inventory.reserve(
            product_id=line.product_id,
            quantity=line.quantity,
        )

    repository.add(order)

    event_bus.publish(OrderPlaced.from_order(order))


# -----------------------------
# Event handlers
# -----------------------------


def send_confirmation_email(event: object) -> None:
    if not isinstance(event, OrderPlaced):
        return

    print(f"Sending confirmation email for order {event.order_id}")


def update_loyalty_points(event: object) -> None:
    if not isinstance(event, OrderPlaced):
        return

    print(f"Updating loyalty points for customer {event.customer_id}")


def record_order_analytics(event: object) -> None:
    if not isinstance(event, OrderPlaced):
        return

    print(f"Recording analytics for order {event.order_id}")


def send_partner_webhook(event: object) -> None:
    if not isinstance(event, OrderPlaced):
        return

    print(f"Sending partner webhook for order {event.order_id}")


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


class InMemoryEventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(
            event_type,
            [],
        ).append(handler)

    def publish(self, event: object) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)


# -----------------------------
# Composition
# -----------------------------


def configure_event_bus() -> InMemoryEventBus:
    event_bus = InMemoryEventBus()

    event_bus.subscribe(
        OrderPlaced,
        send_confirmation_email,
    )
    event_bus.subscribe(
        OrderPlaced,
        update_loyalty_points,
    )
    event_bus.subscribe(
        OrderPlaced,
        record_order_analytics,
    )
    event_bus.subscribe(
        OrderPlaced,
        send_partner_webhook,
    )

    return event_bus


# -----------------------------
# Demo
# -----------------------------


def main() -> None:
    repository = InMemoryOrderRepository()
    inventory = InMemoryInventoryService()
    event_bus = configure_event_bus()

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
        event_bus=event_bus,
    )

    print(f"Placed order with total: €{order.total}")


if __name__ == "__main__":
    main()
