from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QFileDialog,
    QMessageBox,
)

from PySide6.QtGui import QAction

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

from serializer.graph_serializer import (
    GraphSerializer,
)

from serializer.graph_loader import GraphLoader

from registry.plugin_manager import (
    PluginManager,
)


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

        self.setup_menu()
        self.setup_docks()

        self.plugin_manager = PluginManager()

        self.plugin_manager.load_plugins()

        self.create_demo_graph()

        self.compile_graph()

    def setup_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        new_action = QAction(
            "New Project",
            self,
        )

        save_action = QAction(
            "Save Project",
            self,
        )

        load_action = QAction(
            "Load Project",
            self,
        )

        undo_action = QAction(
            "Undo",
            self,
        )

        redo_action = QAction(
            "Redo",
            self,
        )

        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")

        undo_action.triggered.connect(
            self.scene.history.undo
        )

        redo_action.triggered.connect(
            self.scene.history.redo
        )

        file_menu.addSeparator()

        file_menu.addAction(undo_action)
        file_menu.addAction(redo_action)

        new_action.triggered.connect(
            self.new_project
        )

        save_action.triggered.connect(
            self.save_project
        )

        load_action.triggered.connect(
            self.load_project
        )

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

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

    def clear_graph(self):
        self.scene.clear()

        self.runtime_graph = RuntimeGraph()

    def new_project(self):
        self.clear_graph()

        self.compile_graph()

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Template Graph (*.tgraph)",
        )

        if not path:
            return

        GraphSerializer.save_to_file(
            self.scene,
            path,
        )

        QMessageBox.information(
            self,
            "Saved",
            "Project saved successfully",
        )

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Project",
            "",
            "Template Graph (*.tgraph)",
        )

        if not path:
            return

        data = GraphSerializer.load_from_file(
            path
        )

        GraphLoader.load(
            self,
            data,
        )

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

    def auto_layout_graph(self):
        self.runtime_graph.auto_layout()

        for item in self.scene.items():
            if not hasattr(item, "runtime_node"):
                continue

            x, y = item.runtime_node.position

            item.setPos(x, y)