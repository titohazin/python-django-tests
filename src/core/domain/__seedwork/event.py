from abc import ABC
import abc
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, TypeVar, Optional
import typing


D = TypeVar('D')


@dataclass(slots=True, frozen=True)
class EventInterface(Generic[D], ABC):

    event_data: dict | D = None
    occurred_at: Optional[datetime] = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.occurred_at:
            object.__setattr__(self, 'occurred_at', datetime.now())


class EventHandlerInterface(ABC):

    @abc.abstractmethod
    def handle(self, event: EventInterface) -> None:
        ...


class EventDispatcher:

    __instance: 'EventDispatcher' = None

    @classmethod
    @property
    def instance(cls) -> 'EventDispatcher':
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
        return cls.__instance

    def __init__(self):
        raise TypeError("EventDispatcher can not be instantiated " +  # noqa: W504
                        "because it is a singleton. Use EventDispatcher.instance instead.")

    _handlers: typing.Dict[str, list] = {}

    def notify(self, event: EventInterface) -> None:
        event_name = event.__class__.__name__
        if event_name in self._handlers:
            for handler in self._handlers[event_name]:
                handler.handle(event)

    def register(self, event_name: str, handler: EventHandlerInterface) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def unregister(self, event_name: str, handler: EventHandlerInterface) -> None:
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
            if len(self._handlers[event_name]) == 0:
                del self._handlers[event_name]

    def unregister_all(self) -> None:
        self._handlers = {}
