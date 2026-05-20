from graph.pin import Pin
from core.type_system import EXEC_TYPE


class ExecutionPin(Pin):
    def __init__(self, name: str, direction: str):
        super().__init__(name, direction, EXEC_TYPE)