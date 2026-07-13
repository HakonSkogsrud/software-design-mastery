from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


@dataclass(frozen=True)
class PickingTask:
    id: str
    product_id: str
    quantity: int
    destination: str


@dataclass(frozen=True)
class Route:
    robot_id: str
    waypoints: tuple[str, ...]


@dataclass(frozen=True)
class OperationContext:
    operation_id: str
    initiated_by: str


class Logger(Protocol):
    def info(self, message: str, *args: object) -> None: ...


class Metrics(Protocol):
    def increment(self, name: str) -> None: ...


class InventoryService(Protocol):
    def reserve(
        self,
        product_id: str,
        quantity: int,
        task_id: str,
    ) -> None: ...


class RoutePlanner(Protocol):
    def calculate(
        self,
        task: PickingTask,
        robot_id: str,
    ) -> Route: ...


class RobotGateway(Protocol):
    def dispatch(
        self,
        task: PickingTask,
        route: Route,
    ) -> None: ...


class TaskRepository(Protocol):
    def save(self, task: PickingTask) -> None: ...

    def mark_completed(self, task_id: str) -> None: ...


class ConsoleLogger:
    def info(self, message: str, *args: object) -> None:
        if args:
            message = message % args

        print(f"INFO: {message}")


class InMemoryMetrics:
    def __init__(self) -> None:
        self.counters: dict[str, int] = {}

    def increment(self, name: str) -> None:
        self.counters[name] = self.counters.get(name, 0) + 1


class InMemoryInventoryService:
    def __init__(self) -> None:
        self.reservations: list[tuple[str, int, str]] = []

    def reserve(
        self,
        product_id: str,
        quantity: int,
        task_id: str,
    ) -> None:
        self.reservations.append((product_id, quantity, task_id))


class SimpleRoutePlanner:
    def calculate(
        self,
        task: PickingTask,
        robot_id: str,
    ) -> Route:
        return Route(
            robot_id=robot_id,
            waypoints=(
                "storage",
                "main-lane",
                task.destination,
            ),
        )


class InMemoryRobotGateway:
    def __init__(self) -> None:
        self.dispatched_commands: list[tuple[PickingTask, Route]] = []

    def dispatch(
        self,
        task: PickingTask,
        route: Route,
    ) -> None:
        self.dispatched_commands.append((task, route))


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self.tasks: dict[str, PickingTask] = {}
        self.completed_task_ids: set[str] = set()

    def save(self, task: PickingTask) -> None:
        self.tasks[task.id] = task

    def mark_completed(self, task_id: str) -> None:
        self.completed_task_ids.add(task_id)


def create_picking_task(
    product_id: str,
    quantity: int,
    destination: str,
) -> PickingTask:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    return PickingTask(
        id=str(uuid4()),
        product_id=product_id,
        quantity=quantity,
        destination=destination,
    )


class PickingOperation:
    def __init__(
        self,
        inventory: InventoryService,
        route_planner: RoutePlanner,
        robot_gateway: RobotGateway,
        task_repository: TaskRepository,
        logger: Logger,
        metrics: Metrics,
    ) -> None:
        self.inventory = inventory
        self.route_planner = route_planner
        self.robot_gateway = robot_gateway
        self.task_repository = task_repository
        self.logger = logger
        self.metrics = metrics

    def execute(
        self,
        context: OperationContext,
        product_id: str,
        quantity: int,
        destination: str,
        robot_id: str,
    ) -> PickingTask:
        self._log(
            context,
            "Starting picking operation for product %s",
            product_id,
        )
        self.metrics.increment("picking_operation.started")

        task = create_picking_task(
            product_id=product_id,
            quantity=quantity,
            destination=destination,
        )

        self.task_repository.save(task)
        self.metrics.increment("picking_task.created")

        self.inventory.reserve(
            product_id=task.product_id,
            quantity=task.quantity,
            task_id=task.id,
        )

        route = self.route_planner.calculate(
            task=task,
            robot_id=robot_id,
        )
        self.metrics.increment("route.calculated")

        self.robot_gateway.dispatch(
            task=task,
            route=route,
        )

        self.task_repository.mark_completed(task.id)
        self.metrics.increment("picking_operation.completed")

        self._log(
            context,
            "Completed picking task %s",
            task.id,
        )

        return task

    def _log(
        self,
        context: OperationContext,
        message: str,
        *args: object,
    ) -> None:
        self.logger.info(
            "[operation=%s] [initiated_by=%s] " + message,
            context.operation_id,
            context.initiated_by,
            *args,
        )


def main() -> None:
    inventory = InMemoryInventoryService()
    route_planner = SimpleRoutePlanner()
    robot_gateway = InMemoryRobotGateway()
    task_repository = InMemoryTaskRepository()
    metrics = InMemoryMetrics()

    operation = PickingOperation(
        inventory=inventory,
        route_planner=route_planner,
        robot_gateway=robot_gateway,
        task_repository=task_repository,
        logger=ConsoleLogger(),
        metrics=metrics,
    )

    context = OperationContext(
        operation_id=str(uuid4()),
        initiated_by="operator-42",
    )

    task = operation.execute(
        context=context,
        product_id="product-123",
        quantity=4,
        destination="packing-station-2",
        robot_id="robot-7",
    )

    print()
    print("Result")
    print("------")
    print(f"Task: {task}")
    print(f"Reservations: {inventory.reservations}")
    print(f"Dispatched commands: {robot_gateway.dispatched_commands}")
    print(f"Completed tasks: {task_repository.completed_task_ids}")
    print(f"Metrics: {metrics.counters}")


if __name__ == "__main__":
    main()
