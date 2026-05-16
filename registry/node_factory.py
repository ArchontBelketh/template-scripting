from registry.node_registry import NODE_REGISTRY


class NodeFactory:
    @staticmethod
    def create(node_type: str, **kwargs):
        cls = NODE_REGISTRY[node_type]

        return cls(**kwargs)