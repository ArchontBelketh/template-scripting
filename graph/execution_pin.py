from graph.pin import Pin

from core.type_system import EXEC_TYPE


class ExecutionPin(Pin):
    def __init__(
        self,
        name,
        is_input,
        owner=None,
    ):
        super().__init__(
            name=name,
            pin_type=EXEC_TYPE,
            is_input=is_input,
            owner=owner,
        )