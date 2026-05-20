from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from graph.connection import Connection
    from core.type_system import TypeInfo


class Pin:
    def __init__(self, name: str, direction: str, pin_type: "TypeInfo"):
        self.name: str = name
        self.direction: str = direction  # "input" или "output"
        self.pin_type: "TypeInfo" = pin_type
        self.inferred_type: Optional["TypeInfo"] = None
        self.node = None  # Заполняется при добавлении в ноду
        self.connections: List["Connection"] = []

    @property
    def effective_type(self) -> "TypeInfo":
        """Возвращает выведенный тип, если он есть, иначе базовый объявленный."""
        if self.direction == "input" and self.connections:
            # Входной пин наследует тип от присоединенного выхода
            source_pin = self.connections[0].source_pin
            return source_pin.effective_type
        return self.inferred_type if self.inferred_type else self.pin_type

    def is_connected(self) -> bool:
        return len(self.connections) > 0