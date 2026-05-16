from graph.pin import Pin


class DataPin(Pin):
    def __init__(
        self,
        name,
        data_type,
        is_input,
    ):
        super().__init__(
            name=name,
            pin_type=data_type,
            is_input=is_input,
        )