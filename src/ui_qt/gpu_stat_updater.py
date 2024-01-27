from PyQt6.QtCore import QThread, QTimer
from gpu.gpu import GPU
from PyQt6.QtWidgets import QWidget
from datetime import datetime


class StatUpdater(QThread):
    def __init__(self, gpu: GPU) -> None:
        super().__init__()

        self.__gpu = gpu
        self.__widgets = []

        self.__scheduler = QTimer()
        self.__scheduler.timeout.connect(self.start)
        self.__scheduler.setInterval(1000)
        self.__scheduler.start()

    def run(self) -> None:
        data = self.__gpu.get_sensor_data()
        time = datetime.now().strftime("%H.%M.%S")
        for widget in self.__widgets:
            widget.update_signal.emit((data[widget.data_property_id], time))

    def add_widget(self, widget: QWidget) -> None:
        self.__widgets.append(widget)

    def set_update_rate(self, msec: int) -> None:
        self.__scheduler.setInterval(msec)
