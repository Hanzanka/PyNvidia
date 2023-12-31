from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QFrame
from PyQt6.QtGui import QIcon, QPalette, QColor
from src.ui_qt.side_panel import SidePanel
from src.ui_qt.home_frame import HomeFrame
from src.utils.utils import get_path
from src.ui_qt.gpu_chart_frame import GPUChartFrame


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
        
        self.__test = GPUChartFrame()
        
        self.__main_frame = None
        self.__main_return_to = None

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setSpacing(7)
        
        self.__layout.addWidget(self.__home_frame)
        self.set_main_frame(self.__test)
        
        self.__top_frame.setLayout(self.__layout)
        
        self.__top_frame.show()
        
        self.exec()

    def set_main_frame(self, frame: QFrame) -> None:
        if self.__main_frame is not None:
            self.__main_return_to = self.__main_frame
            self.__layout.removeWidget(self.__main_frame)
            self.__main_frame.setParent(None)
        self.__main_frame = frame
        self.__layout.addWidget(self.__main_frame)
