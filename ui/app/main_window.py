from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
)

from PySide6.QtCore import Qt

from ui.editor.graph_scene import GraphScene
from ui.editor.graph_view import GraphView
from ui.editor.node_item import NodeItem
from ui.editor.connection_item import ConnectionItem

from ui.widgets.node_palette import NodePalette
from ui.widgets.inspector_panel import InspectorPanel
from ui.widgets.code_preview import CodePreview

from ui.node_metadata import NODE_METADATA

from ui.runtime.runtime_graph import RuntimeGraph

from compiler.graph_compiler import GraphCompiler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Python Blueprint System"
        )

        self.resize(1800, 1000)

        self.scene = GraphScene()
        self.scene.main_window = self

        self.view = GraphView(self.scene)

        self.runtime_graph = RuntimeGraph()

        self.setCentralWidget(self.view)

        self.setup_docks()

        self.create_demo_graph()

        self.compile_graph()

    def setup_docks(self):
        self.palette = NodePalette()

        self.palette.list_widget.itemDoubleClicked.connect(
            self.create_node_from_palette
        )

        palette_dock = QDockWidget("Palette")
        palette_dock.setWidget(self.palette)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            palette_dock,
        )

        self.inspector = InspectorPanel()

        inspector_dock = QDockWidget("Inspector")
        inspector_dock.setWidget(self.inspector)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            inspector_dock,
        )

        self.preview = CodePreview()

        preview_dock = QDockWidget("Code Preview")
        preview_dock.setWidget(self.preview)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            preview_dock,
        )

    def create_node_from_palette(self):
        node_type = (
            self.palette.get_selected_node_type()
        )

        if not node_type:
            return

        center = self.view.mapToScene(
            self.view.viewport().rect().center()
        )

        self.create_node(
            node_type,
            center.x(),
            center.y(),
        )

    def create_node(
        self,
        node_type,
        x,
        y,
        properties=None,
    ):
        metadata = NODE_METADATA[node_type]

        node = NodeItem(
            node_type,
            metadata["title"],
            metadata["inputs"],
            metadata["outputs"],
        )

        node.properties = properties or {}

        node.setPos(x, y)

        self.scene.addItem(node)

        self.runtime_graph.create_node_from_item(node)

        runtime_node = node.runtime_node

        for index, pin in enumerate(node.inputs):
            pin.runtime_pin = runtime_node.input_pins[index]

        for index, pin in enumerate(node.outputs):
            pin.runtime_pin = runtime_node.output_pins[index]

        return node

    def create_connection_between_pins(
        self,
        pin_a,
        pin_b,
    ):
        if pin_a.is_input:
            input_pin = pin_a
            output_pin = pin_b
        else:
            input_pin = pin_b
            output_pin = pin_a

        connection = ConnectionItem(
            output_pin,
            input_pin,
        )

        output_pin.connections.append(connection)
        input_pin.connections.append(connection)

        self.scene.addItem(connection)

        self.runtime_graph.create_connection(
            output_pin,
            input_pin,
        )

        self.compile_graph()

    def create_demo_graph(self):
        start_node = self.create_node(
            "start",
            0,
            0,
        )

        print_node = self.create_node(
            "print",
            450,
            100,
            {
                "value": "Hello Runtime Graph",
            },
        )

        self.create_connection_between_pins(
            start_node.outputs[0],
            print_node.inputs[0],
        )

    def compile_graph(self):
        compiler = GraphCompiler(
            self.runtime_graph.graph,
        )

        code = compiler.compile()

        self.preview.set_code(code)