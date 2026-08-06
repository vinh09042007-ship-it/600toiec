"""
Simple EventBus for decoupling components.
"""
from typing import Callable, Dict, List, Any
from core.events import Events

class EventBus:
    """
    Manages event subscriptions and emissions using the Events enum.
    """
    def __init__(self) -> None:
        self._subscribers: Dict[Events, List[Callable[..., Any]]] = {}

    def subscribe(self, event_type: Events, callback: Callable[..., Any]) -> None:
        """Subscribe a callback to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: Events, callback: Callable[..., Any]) -> None:
        """Unsubscribe a callback from a specific event type."""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def emit(self, event_type: Events, **kwargs: Any) -> None:
        """Emit an event, calling all subscribed callbacks with kwargs."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(**kwargs)
