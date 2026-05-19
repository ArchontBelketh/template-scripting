from PySide6.QtWidgets import QLabel


class TypeHintWidget(QLabel):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """
            QLabel {
                background: #111827;
                color: #e5e7eb;
                border: 1px solid #374151;
                padding: 4px 8px;
                border-radius: 6px;
            }
            """
        )