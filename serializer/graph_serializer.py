import json


class GraphSerializer:
    @staticmethod
    def serialize(scene):
        nodes_data = []
        connections_data = []

        node_id_map = {}

        for index, item in enumerate(scene.items()):
            if not hasattr(item, "node_type"):
                continue

            node_id = str(index)

            node_id_map[item] = node_id

            nodes_data.append(
                {
                    "id": node_id,
                    "node_type": item.node_type,
                    "x": item.pos().x(),
                    "y": item.pos().y(),
                    "properties": item.properties,
                }
            )

        added_connections = set()

        for item in scene.items():
            if not hasattr(item, "connections"):
                continue

            for connection in item.connections:
                if connection in added_connections:
                    continue

                added_connections.add(connection)

                start_node = connection.start_pin.parentItem()
                end_node = connection.end_pin.parentItem()

                connections_data.append(
                    {
                        "from_node": node_id_map[start_node],
                        "from_pin": connection.start_pin.name,
                        "to_node": node_id_map[end_node],
                        "to_pin": connection.end_pin.name,
                    }
                )

        return {
            "nodes": nodes_data,
            "connections": connections_data,
        }

    @staticmethod
    def save_to_file(scene, path):
        data = GraphSerializer.serialize(scene)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
            )

    @staticmethod
    def load_from_file(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)