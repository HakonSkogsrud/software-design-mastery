from collections.abc import Callable
from typing import Protocol


EventHandler = Callable[[object], None]


class EventBus(Protocol):
    def publish(self, event: object) -> None: ...

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None: ...

    def list_events(self) -> list[object]: ...
