from PyQt6.QtWidgets import (
    QFrame,
    QPushButton,
    QProgressBar,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QThread, QSize
from PyQt6.QtGui import QFont, QMovie
from src.scraper.scraper import NvidiaWebScraper
from src.utils.utils import get_path


class UpdateFrame(QFrame):
    def __init__(self, scraper: NvidiaWebScraper) -> None:
        super().__init__()
        self.setStyleSheet(
            "background-color: #0b0b0b; border-radius: 0px; border-width: 0px"
        )

        self.__scraper = scraper
        self.__scraper_thread = QThread()
        self.__scraper.moveToThread(self.__scraper_thread)

        font = QFont("Fira Code", 8, QFont.Weight.Bold)

        self.__main_layout = QGridLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(7)

        self.__feedback_layout = QHBoxLayout()
        self.__feedback_layout.setContentsMargins(0, 0, 0, 0)
        self.__feedback_layout.setSpacing(5)

        self.__feedback_label = QLabel(text="")
        self.__feedback_label.setFixedHeight(30)
        self.__feedback_label.setStyleSheet("color: white")
        self.__feedback_label.setFont(font)
        self.__feedback_layout.addWidget(self.__feedback_label)

        self.__loading_gif = QMovie(get_path("loading_gif"))
        self.__loading_gif.setScaledSize(QSize(20, 20))
        self.__loading_gif_label = QLabel()
        self.__loading_gif_label.setMovie(self.__loading_gif)

        self.__progress_bar = QProgressBar()
        self.__progress_bar.setFixedHeight(10)
        self.__progress_bar.setMinimum(0)
        self.__progress_bar.setMaximum(0)
        self.__progress_bar.setStyleSheet(
            "QProgressBar {border-radius: 0px; border-radius: 5px; background-color: #0b0b0b; color: transparent}"
            + " QProgressBar::chunk {background-color: #76b900; border-radius: 5px;}"
        )
        self.__progress_bar.setValue(27)

        self.__check_update_button = QPushButton(text="Check For Updates")
        self.__check_update_button.setStyleSheet(
            "QPushButton {background-color: #76b900; border-radius: 5px}"
            + " QPushButton:hover{background-color: #91c733}"
            + " QPushButton:pressed {background-color: #76b900}"
        )
        self.__check_update_button.setFont(font)
        self.__check_update_button.setFixedSize(140, 30)
        self.__main_layout.addWidget(
            self.__check_update_button,
            0,
            2,
            2,
            1,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight,
        )
        self.__check_update_button.clicked.connect(self.__check_update_button_click)

        self.__download_button = QPushButton(text="Download Update")
        self.__download_button.setStyleSheet(
            "QPushButton {background-color: #76b900; border-radius: 5px}"
            + " QPushButton:hover{background-color: #91c733}"
            + " QPushButton:pressed {background-color: #76b900}"
        )
        self.__download_button.setFixedHeight(30)
        self.__download_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.__download_button.setFont(font)
        self.__download_button.clicked.connect(self.__download_button_click)

        self.setLayout(self.__main_layout)

    def __check_update_button_click(self) -> None:
        self.__check_update_button.setEnabled(False)

        self.__feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__feedback_label.setText("Checking For Updates")

        self.__feedback_layout.addWidget(
            self.__loading_gif_label, Qt.AlignmentFlag.AlignCenter
        )
        self.__loading_gif.start()

        if self.__feedback_layout.parent() is None:
            self.__main_layout.addLayout(
                self.__feedback_layout, 1, 0, Qt.AlignmentFlag.AlignLeft
            )

        self.__scraper_thread.wait()

        self.__scraper.check_for_update_signal.connect(self.__check_for_update_complete)
        self.__scraper.check_for_update_error_signal.connect(
            self.__check_for_update_error
        )

        try:
            self.__scraper_thread.started.disconnect()
        except Exception:
            pass
        self.__scraper_thread.started.connect(self.__scraper.check_for_updates)
        self.__scraper_thread.start()

    def __check_for_update_complete(
        self, update_available: bool, available_driver_version: float
    ) -> None:
        self.__main_layout.removeItem(self.__feedback_layout)

        self.__loading_gif.stop()
        self.__feedback_layout.removeWidget(self.__loading_gif_label)
        self.__loading_gif_label.setParent(None)

        self.__feedback_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        if not update_available:
            self.__feedback_label.setText("No Updates Available")
            self.__main_layout.addLayout(
                self.__feedback_layout,
                1,
                0,
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
            )
            self.__check_update_button.setEnabled(True)

        else:
            self.__feedback_label.setText(
                f"Driver Version {available_driver_version} Is Available"
            )
            self.__main_layout.addLayout(
                self.__feedback_layout, 0, 0, Qt.AlignmentFlag.AlignBottom
            )
            self.__main_layout.addWidget(self.__download_button, 1, 0)

        self.__scraper.check_for_update_signal.disconnect(
            self.__check_for_update_complete
        )
        self.__scraper.check_for_update_error_signal.disconnect(
            self.__check_for_update_error
        )
        self.__scraper_thread.quit()

    def __check_for_update_error(self) -> None:
        self.__check_update_button.setEnabled(True)

        self.__feedback_label.setText(
            "Check For Updates Failed\nCheck Your Internet Connection"
        )
        self.__feedback_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.__loading_gif_label.setParent(None)

        self.__scraper.check_for_update_signal.disconnect(
            self.__check_for_update_complete
        )
        self.__scraper.check_for_update_error_signal.disconnect(
            self.__check_for_update_error
        )
        self.__scraper_thread.quit()

    def __download_button_click(self) -> None:
        self.__feedback_label.setText("Downloading Installer")

        self.__progress_bar.setMinimum(0)
        self.__progress_bar.setMaximum(100)
        self.__progress_bar.setValue(0)

        self.__main_layout.replaceWidget(self.__download_button, self.__progress_bar)
        self.__download_button.setParent(None)

        self.__scraper_thread.wait()
        self.__scraper.download_signal.connect(self.__update_download_progress)
        self.__scraper.download_error_signal.connect(self.__download_error)
        self.__scraper.download_complete_signal.connect(self.__download_complete)
        try:
            self.__scraper_thread.started.disconnect()
        except Exception:
            pass
        self.__scraper_thread.started.connect(self.__scraper.download_driver)
        self.__scraper_thread.start()

    def __update_download_progress(
        self,
        percentage: int,
        downloaded: float,
        total_size: float,
        download_rate: float,
    ) -> None:
        self.__progress_bar.setValue(percentage)
        self.__feedback_label.setText(
            f"Downloading Installer {downloaded:.1f} MB / {total_size:.1f} MB - {download_rate:.1f}MB/s",
        )

    def __download_error(self) -> None:
        self.__main_layout.replaceWidget(self.__progress_bar, self.__download_button)
        self.__progress_bar.setParent(None)
        self.__feedback_label.setText("Download Failed\nCheck Your Internet Connection")
        self.__scraper_thread.quit()

    def __download_complete(self, finishing: bool) -> None:
        if finishing:
            self.__feedback_label.setText("Finishing Download")
