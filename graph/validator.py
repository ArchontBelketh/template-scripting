from core.types import (
    DataType,
    is_type_compatible,
)

from core.exceptions import (
    GraphValidationError,
)


class GraphValidator:
    def __init__(self, graph):
        self.graph = graph

    def validate(self):
        errors = []

        errors.extend(
            self.validate_connections()
        )

        errors.extend(
            self.validate_execution_cycles()
        )

        return errors

    def validate_connections(self):
        errors = []

        for connection in self.graph.connections:
            output_pin = connection.output_pin
            input_pin = connection.input_pin

            if not is_type_compatible(
                output_pin.effective_type,
                input_pin.effective_type,
            ):
                errors.append(
                    (
                        f"Type mismatch: "
                        f"{output_pin.type_name} -> "
                        f"{input_pin.type_name}"
                    )
                )

        return errors

    def validate_execution_cycles(self):
        visited = set()
        recursion = set()

        errors = []

        for node in self.graph.nodes:
            if self.walk_cycle(
                node,
                visited,
                recursion,
            ):
                errors.append(
                    "Execution cycle detected"
                )

        return errors

    def walk_cycle(
        self,
        node,
        visited,
        recursion,
    ):
        if node.node_id in recursion:
            return True

        if node.node_id in visited:
            return False

        visited.add(node.node_id)
        recursion.add(node.node_id)

        for pin in node.output_pins:
            if pin.pin_type != DataType.EXECUTION:
                continue

            for connection in pin.connections:
                target = (
                    connection.input_pin.owner
                )

                if self.walk_cycle(
                    target,
                    visited,
                    recursion,
                ):
                    return True

        recursion.remove(node.node_id)

        return False