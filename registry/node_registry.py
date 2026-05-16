NODE_REGISTRY = {}


def register_node(node_class):
    NODE_REGISTRY[node_class.NODE_TYPE] = node_class

    return node_class