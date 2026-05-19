class Command:
    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError


class MoveNodesCommand(Command):
    def __init__(self, nodes, old_positions, new_positions):
        self.nodes = nodes

        self.old_positions = old_positions
        self.new_positions = new_positions

    def undo(self):
        for node in self.nodes:
            pos = self.old_positions[node]

            node.setPos(pos)

    def redo(self):
        for node in self.nodes:
            pos = self.new_positions[node]

            node.setPos(pos)


class CreateNodeCommand(Command):
    def __init__(self, scene, node):
        self.scene = scene
        self.node = node

    def undo(self):
        self.scene.remove_node(self.node)

    def redo(self):
        self.scene.addItem(self.node)


class DeleteNodesCommand(Command):
    def __init__(self, scene, nodes):
        self.scene = scene
        self.nodes = nodes

    def undo(self):
        for node in self.nodes:
            self.scene.addItem(node)

    def redo(self):
        for node in self.nodes:
            self.scene.remove_node(node)