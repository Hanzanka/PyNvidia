from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon, QPalette, QColor
from ui_qt.side_panel import SidePanel
from ui_qt.home_frame import HomeFrame
from utils.utils import get_path
from PyQt6.QtCore import pyqtSlot


class App(QApplication):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        
        self.__palette = QPalette()
        self.__palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(self.__palette)
        
        self.__top_frame = QFrame()
        self.__top_frame.setGeometry(0, 0, 900, 500)
        self.__top_frame.setMinimumSize(900, 500)
        self.__top_frame.setWindowTitle("PyNvidia")
        self.__top_frame.setWindowIcon(QIcon(get_path("icon")))
        self.__top_frame.setStyleSheet("background-color: #050505;")

        self.__side_panel = SidePanel()
        self.__home_frame = HomeFrame()
        
        self.__main_frame = None
        self.__main_return_to = None

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setSpacing(7)
        
        self.__layout.addWidget(self.__side_panel)
        self.set_main_frame(self.__home_frame)
        
        self.__top_frame.setLayout(self.__layout)
        
        self.__top_frame.show()
        
        self.exec()

    @pyqtSlot(QFrame)
    def set_main_frame(self, frame: QFrame) -> None:
        if self.__main_frame is not None:
            self.__main_return_to = self.__main_frame
            self.__layout.removeWidget(self.__main_frame)
            self.__main_frame.setParent(None)
        self.__main_frame = frame
        self.__layout.addWidget(self.__main_frame)
    
    @pyqtSlot()
    def home(self) -> None:
        self.__layout.removeWidget(self.__main_frame)
        self.__main_frame.setParent(None)
        self.__main_frame = self.__home_frame
        self.__layout.addWidget(self.__main_frame)
