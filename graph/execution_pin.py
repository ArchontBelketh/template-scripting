from graph.pin import Pin

from core.types import DataType


class ExecutionPin(Pin):
    def __init__(
        self,
        name,
        is_input,
    ):
        super().__init__(
            name=name,
            pin_type=DataType.EXECUTION,
            is_input=is_input,
        )