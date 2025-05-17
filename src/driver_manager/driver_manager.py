from urllib.request import urlretrieve, urlopen
from gpu.gpu import GPU
from utils.utils import get_path
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from threading import Lock, Timer
from datetime import datetime
import os
import subprocess
import pathlib
import json
import re


class NvidiaDriverManager(QObject):
    check_for_update_signal = pyqtSignal(bool, float, float)
    check_for_update_error_signal = pyqtSignal()

    download_signal = pyqtSignal(int, float, float, float)
    download_error_signal = pyqtSignal()
    download_complete_signal = pyqtSignal(bool)

    extract_error_signal = pyqtSignal()
    extract_complete_signal = pyqtSignal()

    install_error_signal = pyqtSignal()
    install_complete_signal = pyqtSignal()

    def __init__(self, gpu: GPU) -> None:
        super().__init__()
        self.__gpu = gpu
        self.__download_path = get_path("download")
        self.__available_driver_version_str = None
        self.__available_driver_version_float = None
        self.__report_lock = Lock()
        self.__last_update = datetime.now()
        self.__last_size = 0

    def __get_driver_id(self) -> str:
        keys = self.__get_nv_search_keys(
            product_series=self.__gpu.series, product=self.__gpu.product
        )
        url = (
            "processDriver.aspx"
            + f"?psid={keys[0]}"
            + f"&pfid={keys[1]}"
            + "&rpf=1"
            + "&osid=57"
            + "&lid=1"
            + "&lang=en-us"
            + "&ctk=0"
            + "&dtid=1"
            + "&dtcid=1"
        )
        return re.search(
            r"\d+", urlopen(f"https://www.nvidia.com/download/{url}").read().decode()
        ).group()

    @pyqtSlot()
    def check_for_updates(self) -> None:
        try:
            page = json.loads(
                (
                    urlopen(
                        f"https://www.nvidia.com/services/com.nvidia.services/AEMDriversContent/getDownloadDetails?{{%22ddID%22:%22{self.__get_driver_id()}%22}}"
                    )
                    .read()
                    .decode()
                )
            )
        except Exception:
            self.check_for_update_error_signal.emit()
            return
        self.__available_driver_version_str = page["driverDetails"]["IDS"][0][
            "downloadInfo"
        ]["Version"]
        self.__available_driver_version = float(self.__available_driver_version_str)
        self.check_for_update_signal.emit(
            self.__gpu.driver_version != self.__available_driver_version,
            self.__available_driver_version,
            self.__installer_exists(),
        )

    @pyqtSlot()
    def download_driver(self) -> None:
        try:
            if not os.path.isdir(self.__download_path):
                os.makedirs(self.__download_path)
            download_location = (
                self.__download_path + f"{self.__available_driver_version}.exe"
            )
            urlretrieve(
                url="https://us.download.nvidia.com/Windows/"
                + self.__available_driver_version_str
                + "/"
                + self.__available_driver_version_str
                + "-desktop-win10-win11-64bit-international-dch-whql.exe",
                filename=download_location,
                reporthook=self.__update_download_progress,
            )

        except Exception:
            self.download_error_signal.emit()
            self.__delete_unfinished_download()
            return
        self.download_complete_signal.emit(False)

    def __update_download_progress(self, block_num, block_size, total_size) -> None:
        if self.__report_lock.acquire(blocking=False):
            time_now = datetime.now()
            size_now = block_num * block_size
            self.download_signal.emit(
                int(block_num * block_size / total_size * 100),
                block_num * block_size / 1024**2,
                total_size / 1024**2,
                (size_now - self.__last_size)
                / (time_now - self.__last_update).total_seconds()
                / 1024**2,
            )
            self.__last_update = time_now
            self.__last_size = size_now
            Timer(interval=1, function=self.__report_lock.release).start()

        if block_num * block_size >= total_size:
            self.download_signal.emit(
                100,
                total_size / 1024**2,
                total_size / 1024**2,
                0,
            )
            self.download_complete_signal.emit(True)

    def __get_nv_search_keys(self, product_series: str, product: str) -> tuple:
        config_path = (
            str(pathlib.Path(__file__).parents[2]) + "/resources/nv_search_keys.json"
        )
        with open(config_path, "r") as config_file:
            nv_search_keys = json.load(config_file)
            return (
                nv_search_keys["product_series"][product_series],
                nv_search_keys["product_type"][product],
            )

    @pyqtSlot()
    def extract_driver_package(self) -> None:
        sevenz_path = get_path("sevenz")

        folder_path = self.__download_path + str(
            max(
                [
                    float(os.path.splitext(file)[0])
                    for file in os.listdir(self.__download_path)
                ]
            )
        )
        driver_path = folder_path + ".exe"

        if not os.path.exists(folder_path):
            try:
                subprocess.run(
                    args=[
                        sevenz_path,
                        "x",
                        driver_path,
                        "-aoa",
                        "-bso0",
                        "-bsp0",
                        f"-o{folder_path}",
                    ]
                )
            except Exception:
                self.extract_error_signal.emit()

        os.remove(driver_path)
        self.extract_complete_signal.emit()

    def __delete_unfinished_download(self) -> None:
        try:
            os.remove(f"{get_path('download')}{self.__available_driver_version}.exe")
        except Exception:
            pass

    def __installer_exists(self) -> bool:
        return pathlib.Path(
            self.__download_path + str(self.__available_driver_version)
        ).is_dir()

    @pyqtSlot()
    def install_driver(self) -> None:
        try:
            subprocess.run(
                args=[
                    f"{get_path('download')}{self.__available_driver_version}/setup.exe",
                    "-s",
                    "Display.Driver",
                    "HDAudio.Driver",
                ]
            )
        except Exception:
            self.install_error_signal.emit()

        self.install_complete_signal.emit()
