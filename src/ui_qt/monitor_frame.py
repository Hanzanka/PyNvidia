from PyQt6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QGridLayout,
    QProgressBar,
    QLabel,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QCursor
from gpu.gpu import GPU
from ui_qt.gpu_chart_frame import GPUChartFrame
from PyQt6.QtWidgets import QApplication
from ui_qt.gpu_stat_updater import StatUpdater


class MonitorFrame(QFrame):
    class StatUpdater(QThread):
        def __init__(self, frames: list, gpu: GPU) -> None:
            super().__init__()
            self.__gpu = gpu
            self.__frames = frames

        def run(self) -> None:
            data = self.__gpu.get_sensor_data()
            for frame in self.__frames:
                frame.update_signal.emit(data[frame.data_property_id])

    def __init__(self, gpu: GPU) -> None:
        super().__init__()

        self.__gpu = gpu

        self.__updater = StatUpdater(gpu=self.__gpu)

        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 0px; border-width: 0px"
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(250)

        self.__layout = QGridLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(7)

        self.__util = MonitorPropertyFrame(
            title="Utilization", max_value=100, unit="%", data_property_id="utilization"
        )
        self.__layout.addWidget(self.__util, 0, 0, 1, 2)
        self.__updater.add_widget(self.__util)
        self.__util_chart = GPUChartFrame(
            title="Utilization",
            unit="%",
            y_max=100,
            data_property_id="utilization"
        )
        self.__util.mouseReleaseEvent = (
            lambda x: QApplication.instance().set_main_frame(self.__util_chart)
        )
        self.__updater.add_widget(self.__util_chart)

        self.__temp = MonitorPropertyFrame(
            title="Temperature",
            max_value=self.__gpu.target_temperature,
            unit="°C",
            data_property_id="temperature",
        )
        self.__layout.addWidget(self.__temp, 1, 0, 1, 2)
        self.__updater.add_widget(self.__temp)
        self.__temp_chart = GPUChartFrame(
            title="Temperature",
            unit="°C",
            y_max=self.__gpu.target_temperature,
            data_property_id="temperature"
        )
        self.__temp.mouseReleaseEvent = (
            lambda x: QApplication.instance().set_main_frame(self.__temp_chart)
        )
        self.__updater.add_widget(self.__temp_chart)

        self.__clock = MonitorPropertyFrame(
            title="Core Clock",
            max_value=self.__gpu.max_graphics_clock,
            unit="MHz",
            data_property_id="clock",
        )
        self.__layout.addWidget(self.__clock, 2, 0)
        self.__updater.add_widget(self.__clock)
        self.__clock_chart = GPUChartFrame(
            title="Core Clock",
            unit="MHz",
            y_max=self.__gpu.max_graphics_clock,
            data_property_id="clock",
        )
        self.__clock.mouseReleaseEvent = (
            lambda x: QApplication.instance().set_main_frame(self.__clock_chart)
        )
        self.__updater.add_widget(self.__clock_chart)

        self.__vram = MonitorPropertyFrame(
            title="VRAM",
            max_value=self.__gpu.vram_gb,
            unit="GB",
            data_property_id="vram_gb",
        )
        self.__layout.addWidget(self.__vram, 2, 1)
        self.__updater.add_widget(self.__vram)
        self.__vram_chart = GPUChartFrame(
            title="VRAM",
            unit="GB",
            y_max=self.__gpu.vram_gb,
            data_property_id="vram_gb",
        )
        self.__vram.mouseReleaseEvent = (
            lambda x: QApplication.instance().set_main_frame(self.__vram_chart)
        )
        self.__updater.add_widget(self.__vram_chart)

        self.__fan = MonitorPropertyFrame(
            title="Fan Speed", max_value=100, unit="%", data_property_id="fan"
        )
        self.__layout.addWidget(self.__fan, 3, 0)
        self.__updater.add_widget(self.__fan)
        self.__fan_chart = GPUChartFrame(
            title="Fan Speed",
            unit="%",
            y_max=100,
            data_property_id="fan",
        )
        self.__fan.mouseReleaseEvent = lambda x: QApplication.instance().set_main_frame(
            self.__fan_chart
        )
        self.__updater.add_widget(self.__fan_chart)

        self.__power = MonitorPropertyFrame(
            title="Power",
            max_value=self.__gpu.power_limit,
            unit="W",
            data_property_id="power",
        )
        self.__updater.add_widget(self.__power)
        self.__layout.addWidget(self.__power, 3, 1)
        self.__power_chart = GPUChartFrame(
            title="Power",
            unit="W",
            y_max=self.__gpu.power_limit,
            data_property_id="power",
        )
        self.__power.mouseReleaseEvent = (
            lambda x: QApplication.instance().set_main_frame(self.__power_chart)
        )
        self.__updater.add_widget(self.__power_chart)

        self.setLayout(self.__layout)


class MonitorPropertyFrame(QFrame):
    update_signal = pyqtSignal(object)

    def __init__(
        self, title: str, max_value: int | float, unit: str, data_property_id: str
    ) -> None:
        super().__init__()

        self.setStyleSheet("background-color: #121212; border-radius: 5px")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

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
        self.__value.setFixedWidth(50)
        self.__value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__value, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.__progress_bar = QProgressBar()
        self.__progress_bar.setFixedHeight(10)
        self.__progress_bar.setMinimum(0)
        self.__progress_bar.setMaximum(
            max_value if type(max_value) is int else int(max_value * 10)
        )
        self.__progress_bar.setStyleSheet(
            "QProgressBar {border-radius: 2px; background-color: #0b0b0b; color: transparent}"
            + " QProgressBar::chunk {background-color: #76b900; border-radius: 2px;}"
        )
        self.__progress_bar.setValue(100)
        self.__layout.addWidget(self.__progress_bar, 1, 1)

        self.__max = QLabel(f"{max_value}{self.__unit}")
        self.__max.setFont(font)
        self.__max.setFixedWidth(50)
        self.__max.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__max, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.__layout)

        self.update_signal.connect(self.__update_value)

    @property
    def data_property_id(self) -> str:
        return self.__data_property_id

    @pyqtSlot(object)
    def __update_value(self, value) -> None:
        value = value[0]
        self.__value.setText(f"{value}{self.__unit}")
        self.__progress_bar.setValue(value if type(value) is int else int(value * 10))
