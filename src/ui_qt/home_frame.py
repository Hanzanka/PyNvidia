from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from gpu.gpu import GPU
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui_qt.update_frame import UpdateFrame
from ui_qt.monitor_frame import MonitorFrame
from driver_manager.driver_manager import NvidiaDriverManager


class HomeFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 5px; border-width: 0px"
        )

        self.__gpu = GPU(laptop_dev=False)
        self.__driver_manager = NvidiaDriverManager(self.__gpu)

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setSpacing(7)

        font = QFont("Fira Code", 20, QFont.Weight.Bold)

        self.__title = QLabel(text=self.__gpu.full_name)
        self.__title.setFont(font)
        self.__title.setStyleSheet("color: white")
        self.__title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__title)

        self.__layout.addStretch()

        self.__monitor_frame = MonitorFrame(gpu=self.__gpu)
        self.__layout.addWidget(self.__monitor_frame)

        self.__update_frame = UpdateFrame(scraper=self.__driver_manager)
        self.__layout.addWidget(self.__update_frame)

        self.setLayout(self.__layout)
