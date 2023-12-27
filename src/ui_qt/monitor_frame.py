from PyQt6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QGridLayout,
    QProgressBar,
    QLabel,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from src.gpu.gpu import GPU


class MonitorFrame(QFrame):
    def __init__(self, gpu: GPU) -> None:
        super().__init__()

        self.__gpu = gpu

        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 0px; border-width: 0px"
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(250)

        self.__layout = QGridLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(7)

        self.__items = []

        self.__util = MonitorPropertyFrame(
            title="Utilization", max_value=100, unit="%", data_property_id="utilization"
        )
        self.__layout.addWidget(self.__util, 0, 0, 1, 2)
        self.__items.append(self.__util)

        self.__temp = MonitorPropertyFrame(
            title="Temperature",
            max_value=self.__gpu.target_temperature,
            unit="°C",
            data_property_id="temperature",
        )
        self.__layout.addWidget(self.__temp, 1, 0, 1, 2)
        self.__items.append(self.__temp)

        self.__clock = MonitorPropertyFrame(
            title="Core Clock",
            max_value=self.__gpu.max_graphics_clock,
            unit="MHz",
            data_property_id="clock",
        )
        self.__layout.addWidget(self.__clock, 2, 0)
        self.__items.append(self.__clock)

        self.__vram = MonitorPropertyFrame(
            title="VRAM", max_value=self.__gpu.vram_gb, unit="GB", data_property_id="vram_gb"
        )
        self.__layout.addWidget(self.__vram, 2, 1)
        self.__items.append(self.__vram)

        self.__fan = MonitorPropertyFrame(
            title="Fan Speed", max_value=100, unit="%", data_property_id="fan"
        )
        self.__layout.addWidget(self.__fan, 3, 0)
        self.__items.append(self.__fan)

        self.__power = MonitorPropertyFrame(
            title="Power",
            max_value=self.__gpu.power_limit,
            unit="W",
            data_property_id="power",
        )
        self.__layout.addWidget(self.__power, 3, 1)
        self.__items.append(self.__power)

        self.setLayout(self.__layout)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update_data)
        self.__timer.start(1000)

    def __update_data(self) -> None:
        data = self.__gpu.get_sensor_data()
        for item in self.__items:
            item.update_value(data[item.data_property_id])


class MonitorPropertyFrame(QFrame):
    def __init__(
        self, title: str, max_value: int | float, unit: str, data_property_id: str
    ) -> None:
        super().__init__()

        self.setStyleSheet("background-color: #121212; border-radius: 5px")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        font = QFont("Fira Code", 8, QFont.Weight.Bold)

        self.__unit = unit
        self.__data_property_id = data_property_id

        self.__layout = QGridLayout()
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setSpacing(7)

        self.__title = QLabel(title)
        self.__title.setFont(font)
        self.__title.setFixedHeight(15)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__title, 0, 1, Qt.AlignmentFlag.AlignCenter)

        self.__value = QLabel(f"0{self.__unit}")
        self.__value.setFont(font)
        self.__value.setFixedWidth(55)
        self.__value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__value, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.__progress_bar = QProgressBar()
        self.__progress_bar.setFixedHeight(10)
        self.__progress_bar.setMinimum(0)
        self.__progress_bar.setMaximum(max_value if type(max_value) is int else int(max_value * 10))
        self.__progress_bar.setStyleSheet(
            "QProgressBar {border-radius: 5px; background-color: #0b0b0b; color: transparent}"
            + " QProgressBar::chunk {background-color: #76b900; border-radius: 5px;}"
        )
        self.__progress_bar.setValue(100)
        self.__layout.addWidget(self.__progress_bar, 1, 1)

        self.__max = QLabel(f"{max_value}{self.__unit}")
        self.__max.setFont(font)
        self.__max.setFixedWidth(55)
        self.__max.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__max, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.__layout)

    @property
    def data_property_id(self) -> str:
        return self.__data_property_id

    def update_value(self, value) -> None:
        self.__value.setText(f"{value}{self.__unit}")
        self.__progress_bar.setValue(value if type(value) is int else int(value * 10))
