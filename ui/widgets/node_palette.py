from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
)

from ui.node_metadata import NODE_METADATA


class NodePalette(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Node Palette")

        self.list_widget = QListWidget()

        self.node_types = []

        for node_type, metadata in NODE_METADATA.items():
            self.list_widget.addItem(
                metadata["title"]
            )

            self.node_types.append(node_type)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)

    def get_selected_node_type(self):
        row = self.list_widget.currentRow()

        if row < 0:
            return None

        return self.node_types[row]