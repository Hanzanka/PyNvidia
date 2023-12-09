from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from src.ui_qt.side_panel import SidePanel
from src.ui_qt.home_frame import HomeFrame
from src.utils.utils import get_path


class App(QWidget):
    def __init__(self, argv) -> None:
        self.__app = QApplication(argv)
        super().__init__()

        self.setGeometry(0, 0, 900, 500)
        self.setMinimumSize(900, 500)
        self.setWindowTitle("PyNvidia")
        self.setWindowIcon(QIcon(get_path("icon")))
        self.setStyleSheet("background-color: #050505;")

        self.__side_panel = SidePanel()
        self.__home_frame = HomeFrame()

        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__side_panel)
        self.__layout.addWidget(self.__home_frame)
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setSpacing(7)
        self.setLayout(self.__layout)

        self.show()
        self.__app.exec()
