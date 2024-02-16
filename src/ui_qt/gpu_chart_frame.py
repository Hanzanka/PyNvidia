from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pyqtgraph as QGraph
from pyqtgraph import GraphicsLayoutWidget
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont, QPen, QColor
import numpy as np


class GPUChartFrame(QFrame):
    update_signal = pyqtSignal(object)

    def __init__(
        self,
        title: str,
        unit: str,
        y_max: int | float,
        data_property_id: str,
    ) -> None:
        super().__init__()
        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 5px; border-width: 0px"
        )

        font = QFont("Fira Code", 8, QFont.Weight.Bold)
        pen = QPen(QColor("white"))
        self.__curve_pen = QGraph.mkPen("#76b900", width=1)

        self.__unit = unit
        self.__data_property_id = data_property_id

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(5, 5, 5, 5)
        self.__layout.setSpacing(7)

        self.__graph = GraphicsLayoutWidget()
        self.__graph.setBackground("#0b0b0b")

        self.__plot = self.__graph.addPlot()
        self.__plot.setTitle("Based", color="white")
        self.__plot.titleLabel.item.setFont(font)
        self.__plot.getViewBox().setBackgroundColor("#0b0b0b")
        self.__plot.setRange(xRange=(0, 100), yRange=(0, y_max))
        self.__plot.getViewBox().invertX(True)
        self.__plot.setMenuEnabled(False)
        self.__plot.setMouseEnabled(x=False, y=False)
        self.__plot.hideButtons()

        self.__plot.setLabel("bottom", "Last 100 Seconds")
        bottom_axis = self.__plot.getAxis("bottom")
        bottom_axis.label.setFont(font)
        bottom_axis.setTickFont(font)
        bottom_axis.setPen(pen)
        bottom_axis.setTextPen(pen)
        ticks = np.arange(100, -1, -10)
        bottom_axis.setTicks([[(tick, str(tick)) for tick in ticks]])

        self.__plot.setLabel("left", f"{title} ({self.__unit})")
        left_axis = self.__plot.getAxis("left")
        left_axis.label.setFont(font)
        left_axis.setTickFont(font)
        left_axis.setPen(pen)
        left_axis.setTextPen(pen)
        if y_max < 20:
            tick_range = 1
        elif 20 < y_max and y_max < 40:
            tick_range = 5
        elif 40 < y_max and y_max < 200:
            tick_range = 10
        elif 200 < y_max and y_max < 400:
            tick_range = 20
        elif 400 < y_max and y_max < 1000:
            tick_range = 50
        elif 1000 < y_max and y_max < 2000:
            tick_range = 100
        else:
            tick_range = 200
        ticks = np.arange(0, y_max + 10, tick_range)
        left_axis.setTicks([[(tick, str(tick)) for tick in ticks]])

        self.__examine_line = QGraph.InfiniteLine(
            angle=90,
            movable=False,
            pen=QGraph.mkPen("red", width=2, style=Qt.PenStyle.DashLine, dash=[2, 5]),
        )
        self.__plot.addItem(self.__examine_line, ignoreBounds=True)

        self.__y_value = QGraph.TextItem(
            text="", color="white", anchor=(0.5, 0.5), fill=(11, 11, 11, 225)
        )
        self.__y_value.setZValue(2)
        self.__plot.addItem(self.__y_value, ignoreBounds=True)

        self.__x_value = QGraph.TextItem(
            text="", color="white", anchor=(0.5, 0.5), fill=(11, 11, 11, 225)
        )
        self.__x_value.setZValue(1)
        self.__plot.addItem(self.__x_value, ignoreBounds=True)

        self.__x_data = np.array([])
        self.__y_data = np.array([])
        self.__x_times = np.zeros([], dtype="U8")

        self.__curve = self.__plot.plot(
            self.__x_data, self.__y_data, pen=self.__curve_pen
        )

        self.__proxy = QGraph.SignalProxy(
            self.__plot.scene().sigMouseMoved, rateLimit=60, slot=self.__mouse_moved
        )

        self.__layout.addWidget(self.__graph)
        self.setLayout(self.__layout)

        self.update_signal.connect(self.__update_data)

    @property
    def data_property_id(self) -> str:
        return self.__data_property_id

    @pyqtSlot(tuple)
    def __mouse_moved(self, evt):
        pos = evt[0]
        if self.__plot.sceneBoundingRect().contains(pos):
            mousePoint = self.__plot.vb.mapSceneToView(pos)
            nearest_index = np.abs(self.__x_data - mousePoint.x()).argmin()
            nearest_x = self.__x_data[nearest_index]
            nearest_y = self.__y_data[nearest_index]
            self.__examine_line.setPos(nearest_x)
            self.__y_value.setText(f"{nearest_y}{self.__unit}")
            self.__y_value.setPos(nearest_x, nearest_y)
            self.__x_value.setText(f"{self.__x_times[nearest_x]}")
            self.__x_value.setPos(nearest_x, 0)

    @pyqtSlot(object)
    def __update_data(self, value) -> None:
        time = value[1]
        value = value[0]

        if len(self.__y_data) == 101:
            self.__y_data = np.roll(self.__y_data, 1)
            self.__y_data[0] = value
            self.__x_times = np.roll(self.__x_times, 1)
            self.__x_times[0] = time

        elif len(self.__y_data) != 0:
            self.__y_data = np.insert(self.__y_data, 0, value)
            self.__x_data = np.append(self.__x_data, self.__x_data[-1] + 1)
            self.__x_times = np.insert(self.__x_times, 0, time)
        
        else:
            self.__x_data = np.array([0])
            self.__y_data = np.array([value])
            self.__x_times = np.array([time], dtype="U8")

        self.__curve.setData(self.__x_data, self.__y_data)

        line_pos = self.__examine_line.getPos()[0]
        self.__y_value.setText(f"{self.__y_data[line_pos]}{self.__unit}")
        self.__y_value.setPos(line_pos, self.__y_data[line_pos])
        self.__x_value.setText(f"{self.__x_times[line_pos]}")

        self.__plot.setTitle(
            f"Current: {value}{self.__unit} | "
            + f"Min: {self.__y_data.min()}{self.__unit} | "
            + f"Max: {self.__y_data.max()}{self.__unit} | "
            + f"Avg: {np.average(self.__y_data):.1f}{self.__unit}",
            color="white",
        )
