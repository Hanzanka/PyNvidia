from urllib.request import urlretrieve, urlopen
from src.gpu.gpu import GPU
import os
from src.utils.utils import get_path
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from threading import Lock, Timer
from src.utils.utils import delete_unfinished_download, get_nv_search_keys
from bs4 import BeautifulSoup
from datetime import datetime


class NvidiaWebScraper(QObject):
    check_for_update_signal = pyqtSignal(bool, float)
    check_for_update_error_signal = pyqtSignal()

    download_signal = pyqtSignal(int, float, float, float)
    download_error_signal = pyqtSignal()
    download_complete_signal = pyqtSignal(bool)

    def __init__(self, gpu: GPU) -> None:
        super().__init__()
        self.__gpu = gpu
        self.__download_path = get_path("download")
        self.__available_driver_version = None
        self.__report_lock = Lock()
        self.__last_update = datetime.now()
        self.__last_size = 0

    def __get_driver_url(self) -> str:
        keys = get_nv_search_keys(
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
        return f"https://www.nvidia.com/download/{urlopen(f'https://www.nvidia.com/download/{url}').read().decode()}"

    @pyqtSlot()
    def check_for_updates(self) -> None:
        try:
            page = urlopen(self.__get_driver_url()).read().decode()
        except Exception:
            self.check_for_update_error_signal.emit()
            return
        soup = BeautifulSoup(page, "html.parser")
        td = soup.find("td", {"id": "tdVersion"})
        self.__available_driver_version = float(td.text.split()[0])
        self.check_for_update_signal.emit(
            self.__gpu.driver_version != self.__available_driver_version,
            self.__available_driver_version,
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
                + str(self.__available_driver_version)
                + "/"
                + str(self.__available_driver_version)
                + "-desktop-win10-win11-64bit-international-dch-whql.exe",
                filename=download_location,
                reporthook=self.__update_download_progress,
            )
        except Exception:
            self.download_error_signal.emit()
            delete_unfinished_download(driver_version=self.__available_driver_version)
            return
        self.download_complete_signal.emit(None)

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
            Timer(interval=0.5, function=self.__report_lock.release).start()

        if block_num * block_size >= total_size:
            self.download_complete_signal.emit(True)


if __name__ == "__main__":
    gpu = GPU(laptop_dev=True)
    scraper = NvidiaWebScraper(gpu=gpu)
