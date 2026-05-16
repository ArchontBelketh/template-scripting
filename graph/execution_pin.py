from graph.pin import Pin


class ExecutionPin(Pin):
    def __init__(
        self,
        name,
        is_input,
    ):
        super().__init__(
            name=name,
            pin_type="execution",
            is_input=is_input,
        )