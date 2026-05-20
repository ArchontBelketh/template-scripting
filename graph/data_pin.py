from graph.pin import Pin
from core.type_system import TypeInfo, ANY_TYPE


class DataPin(Pin):
    def __init__(self, name: str, direction: str, pin_type: TypeInfo = ANY_TYPE, default_value: str = ""):
        super().__init__(name, direction, pin_type)
        self.default_value: str = default_value