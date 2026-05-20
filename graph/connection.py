from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graph.pin import Pin


class Connection:
    def __init__(self, source_pin: "Pin", target_pin: "Pin"):
        self.source_pin: "Pin" = source_pin
        self.target_pin: "Pin" = target_pin

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return self.source_pin == other.source_pin and self.target_pin == other.target_pin