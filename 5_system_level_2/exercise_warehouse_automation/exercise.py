import logging
from dataclasses import dataclass
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("warehouse")


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


class InventoryService:
    def __init__(self) -> None:
        self.reservations: list[tuple[str, int, str]] = []

    def reserve(
        self,
        product_id: str,
        quantity: int,
        task_id: str,
    ) -> None:
        logger.info(
            "Reserving %s units of %s for task %s",
            quantity,
            product_id,
            task_id,
        )

        self.reservations.append((product_id, quantity, task_id))


class RoutePlanner:
    def calculate(
        self,
        task: PickingTask,
        robot_id: str,
    ) -> Route:
        logger.info(
            "Calculating route for robot %s",
            robot_id,
        )

        return Route(
            robot_id=robot_id,
            waypoints=(
                "storage",
                "main-lane",
                task.destination,
            ),
        )


class RobotGateway:
    def __init__(self) -> None:
        self.dispatched_commands: list[tuple[PickingTask, Route]] = []

    def dispatch(
        self,
        task: PickingTask,
        route: Route,
    ) -> None:
        logger.info(
            "Sending task %s to robot %s",
            task.id,
            route.robot_id,
        )

        self.dispatched_commands.append((task, route))


class TaskRepository:
    def __init__(self) -> None:
        self.tasks: dict[str, PickingTask] = {}
        self.completed_task_ids: set[str] = set()

    def save(self, task: PickingTask) -> None:
        logger.info(
            "Saving picking task %s",
            task.id,
        )

        self.tasks[task.id] = task

    def mark_completed(self, task_id: str) -> None:
        logger.info(
            "Marking task %s as completed",
            task_id,
        )

        self.completed_task_ids.add(task_id)


def create_picking_task(
    product_id: str,
    quantity: int,
    destination: str,
) -> PickingTask:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    task = PickingTask(
        id=str(uuid4()),
        product_id=product_id,
        quantity=quantity,
        destination=destination,
    )

    logger.info(
        "Created picking task %s",
        task.id,
    )

    return task


def execute_picking_operation(
    product_id: str,
    quantity: int,
    destination: str,
    robot_id: str,
    inventory: InventoryService,
    route_planner: RoutePlanner,
    robot_gateway: RobotGateway,
    task_repository: TaskRepository,
) -> PickingTask:
    operation_id = str(uuid4())

    logger.info(
        "[operation=%s] Starting picking operation",
        operation_id,
    )

    task = create_picking_task(
        product_id=product_id,
        quantity=quantity,
        destination=destination,
    )

    task_repository.save(task)

    inventory.reserve(
        product_id=task.product_id,
        quantity=task.quantity,
        task_id=task.id,
    )

    route = route_planner.calculate(
        task=task,
        robot_id=robot_id,
    )

    robot_gateway.dispatch(
        task=task,
        route=route,
    )

    task_repository.mark_completed(task.id)

    logger.info(
        "[operation=%s] Completed picking task %s",
        operation_id,
        task.id,
    )

    return task


def main() -> None:
    inventory = InventoryService()
    route_planner = RoutePlanner()
    robot_gateway = RobotGateway()
    task_repository = TaskRepository()

    task = execute_picking_operation(
        product_id="product-123",
        quantity=4,
        destination="packing-station-2",
        robot_id="robot-7",
        inventory=inventory,
        route_planner=route_planner,
        robot_gateway=robot_gateway,
        task_repository=task_repository,
    )

    print()
    print("Result")
    print("------")
    print(f"Task: {task}")
    print(f"Reservations: {inventory.reservations}")
    print(f"Dispatched commands: {robot_gateway.dispatched_commands}")
    print(f"Completed tasks: {task_repository.completed_task_ids}")


if __name__ == "__main__":
    main()
