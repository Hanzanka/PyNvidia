from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


class SidePanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 5px; border-width: 0px"
        )
        self.setFixedWidth(200)

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(7)
        self.__layout.setContentsMargins(7, 7, 7, 7)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        font = QFont("Fira Code", 10, QFont.Weight.Bold)

        self.__home_button = QPushButton(text="Home")
        self.__home_button.setFixedHeight(30)
        self.__home_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.__home_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__home_button.setFont(font)
        self.__home_button.setStyleSheet(
            "QPushButton {background-color: #76b900; color: #0b0b0b} QPushButton:hover{background-color: #91c733} QPushButton:pressed {background-color: #76b900}"
        )
        self.__home_button.clicked.connect(QApplication.instance().home)
        self.__layout.addWidget(self.__home_button)

        self.__settings_button = QPushButton(text="Settings")
        self.__settings_button.setFixedHeight(30)
        self.__settings_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.__settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__settings_button.setFont(font)
        self.__settings_button.setStyleSheet(
            "QPushButton {background-color: #76b900; color: #0b0b0b} QPushButton:hover{background-color: #91c733} QPushButton:pressed {background-color: #76b900}"
        )
        self.__layout.addWidget(self.__settings_button)

        self.__layout.addStretch()

        self.__label = QLabel(text="Made By Ville Einiö\ngithub.com/Hanzanka")
        self.__label.setFont(font)
        self.__label.setStyleSheet("color: white")
        self.__label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__layout.addWidget(self.__label)
        self.setLayout(self.__layout)
