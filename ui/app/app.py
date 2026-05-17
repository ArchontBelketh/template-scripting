import sys

from PySide6.QtWidgets import QApplication

from ui.app.main_window import MainWindow


GLOBAL_STYLE = """
QMainWindow {
    background-color: #1e1f22;
}

QDockWidget {
    color: #e5e7eb;
    font-size: 12px;
}

QWidget {
    background-color: #25262b;
    color: #e5e7eb;
}

QListWidget {
    border: none;
    background-color: #1f2023;
}

QPlainTextEdit {
    background-color: #111214;
    border: 1px solid #3b3d44;
    font-family: Consolas;
    font-size: 14px;
}
"""


def run_app():
    app = QApplication(sys.argv)

    app.setStyleSheet(GLOBAL_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())