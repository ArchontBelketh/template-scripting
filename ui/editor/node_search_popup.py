from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
)

from ui.node_metadata import NODE_METADATA


class NodeSearchPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Node")

        self.resize(350, 500)

        self.selected_node = None

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search node..."
        )

        self.list_widget = QListWidget()

        layout.addWidget(self.search)
        layout.addWidget(self.list_widget)

        self.populate()

        self.search.textChanged.connect(
            self.filter_nodes
        )

        self.list_widget.itemDoubleClicked.connect(
            self.accept_selection
        )

    def populate(self):
        self.list_widget.clear()

        for node_type, metadata in NODE_METADATA.items():
            self.list_widget.addItem(
                f"{metadata['title']} ({node_type})"
            )

    def filter_nodes(self, text):
        self.list_widget.clear()

        text = text.lower()

        for node_type, metadata in NODE_METADATA.items():
            title = metadata["title"]

            combined = (
                title + " " + node_type
            ).lower()

            if text in combined:
                self.list_widget.addItem(
                    f"{title} ({node_type})"
                )

    def accept_selection(self):
        text = self.list_widget.currentItem().text()

        node_type = (
            text.split("(")[-1]
            .replace(")", "")
        )

        self.selected_node = node_type

        self.accept()