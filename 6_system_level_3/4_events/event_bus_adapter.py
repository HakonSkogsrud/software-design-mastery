from domain.event_port import EventHandler


class InMemoryEventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = {}
        self._published_events: list[object] = []

    def subscribe(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        self._published_events.append(event)

        for handler in self._handlers.get(type(event), []):
            handler(event)

    def list_events(self) -> list[object]:
        return list(self._published_events)
