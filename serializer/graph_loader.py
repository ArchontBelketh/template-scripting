class GraphLoader:
    @staticmethod
    def load(main_window, data):
        main_window.clear_graph()

        created_nodes = {}

        for node_data in data["nodes"]:
            node = main_window.create_node(
                node_type=node_data["node_type"],
                x=node_data["x"],
                y=node_data["y"],
                properties=node_data.get(
                    "properties",
                    {},
                ),
            )

            created_nodes[
                node_data["id"]
            ] = node

        for connection_data in data["connections"]:
            from_node = created_nodes[
                connection_data["from_node"]
            ]

            to_node = created_nodes[
                connection_data["to_node"]
            ]

            output_pin = None
            input_pin = None

            for pin in from_node.outputs:
                if (
                    pin.name
                    == connection_data["from_pin"]
                ):
                    output_pin = pin
                    break

            for pin in to_node.inputs:
                if (
                    pin.name
                    == connection_data["to_pin"]
                ):
                    input_pin = pin
                    break

            if output_pin and input_pin:
                main_window.create_connection_between_pins(
                    output_pin,
                    input_pin,
                )

        main_window.compile_graph()