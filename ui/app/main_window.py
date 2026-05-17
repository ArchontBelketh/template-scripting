from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
)

from ui.editor.graph_scene import GraphScene
from ui.editor.graph_view import GraphView
from ui.editor.node_item import NodeItem
from ui.editor.connection_item import ConnectionItem

from ui.widgets.node_palette import NodePalette
from ui.widgets.inspector_panel import InspectorPanel
from ui.widgets.code_preview import CodePreview

from ui.node_metadata import NODE_METADATA


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Python Blueprint System"
        )

        self.resize(1800, 1000)

        self.scene = GraphScene()
        self.view = GraphView(self.scene)

        self.setCentralWidget(self.view)

        self.setup_docks()

        self.create_demo_graph()

    def setup_docks(self):
        palette_dock = QDockWidget("Palette")
        palette_dock.setWidget(NodePalette())

        self.addDockWidget(
            1,
            palette_dock,
        )

        inspector_dock = QDockWidget("Inspector")
        inspector_dock.setWidget(InspectorPanel())

        self.addDockWidget(
            2,
            inspector_dock,
        )

        preview_dock = QDockWidget("Code Preview")
        preview_dock.setWidget(CodePreview())

        self.addDockWidget(
            8,
            preview_dock,
        )

    def create_demo_graph(self):
        while_meta = NODE_METADATA["while"]

        while_node = NodeItem(
            while_meta["title"],
            while_meta["inputs"],
            while_meta["outputs"],
        )

        while_node.setPos(0, 0)

        self.scene.addItem(while_node)

        print_meta = NODE_METADATA["print"]

        print_node = NodeItem(
            print_meta["title"],
            print_meta["inputs"],
            print_meta["outputs"],
        )

        print_node.setPos(450, 120)

        self.scene.addItem(print_node)

        connection = ConnectionItem(
            while_node.outputs[0],
            print_node.inputs[0],
        )

        self.scene.addItem(connection)