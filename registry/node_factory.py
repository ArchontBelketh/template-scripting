from registry.node_registry import NODE_REGISTRY


class NodeFactory:
    @staticmethod
    def create(node_type: str, **kwargs):
        if node_type not in NODE_REGISTRY:
            raise ValueError(
                f"Unknown node type: {node_type}"
            )

        cls = NODE_REGISTRY[node_type]

        return cls(**kwargs)