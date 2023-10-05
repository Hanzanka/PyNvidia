from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from gpu.gpu import GPU
from pathlib import Path
from options.options import download_path


class NvidiaWebScraper:
    def __init__(self, gpu: GPU) -> None:
        options = Options()
        options.headless = True
        self.__webdriver = Edge(options=options)
        self.__search_page = "https://www.nvidia.com/download/index.aspx"
        self.__gpu = gpu

    def download_installer(self, reporthook=None) -> None:
        self.__open_search_page()
        link = self.__get_download_link()
        download_location = Path(download_path)
        if not download_location.exists():
            download_location.mkdir()
        download_location = (
            str(download_location.resolve()) + f"/{link.split('/')[4]}.exe"
        )
        if Path(download_location).exists():
            print("File already exists. Skipping download...")
            return
        urlretrieve(url=link, filename=download_location, reporthook=reporthook)

    def check_for_updates(self) -> bool:
        self.__open_search_page()
        driver_version = self.__webdriver.find_element(
            by=By.XPATH, value='//*[@id="tdVersion"]'
        ).text
        return self.__gpu.driver_version != driver_version

    def __open_search_page(self) -> None:
        self.__webdriver.get(self.__search_page)

        Select(
            self.__webdriver.find_element(by=By.ID, value="selProductSeriesType")
        ).select_by_visible_text(text=self.__gpu.type)

        Select(
            webelement=self.__webdriver.find_element(by=By.ID, value="selProductSeries")
        ).select_by_visible_text(text=self.__gpu.series)

        Select(
            webelement=self.__webdriver.find_element(by=By.ID, value="selProductFamily")
        ).select_by_visible_text(text=self.__gpu.product)

        Select(
            webelement=self.__webdriver.find_element(
                by=By.ID, value="selOperatingSystem"
            )
        ).select_by_visible_text(text="Windows 10 64-bit")

        Select(
            webelement=self.__webdriver.find_element(
                by=By.ID, value="ddlDownloadTypeCrdGrd"
            )
        ).select_by_visible_text(text="Game Ready Driver (GRD)")

        Select(
            webelement=self.__webdriver.find_element(by=By.ID, value="ddlLanguage")
        ).select_by_visible_text(text="English (US)")

        self.__webdriver.execute_script("javascript: GetDriver();")

    def __get_download_link(self) -> str:
        self.__webdriver.get(
            self.__webdriver.find_element(
                by=By.XPATH, value='//*[@id="lnkDwnldBtn"]'
            ).get_attribute(name="href")
        )

        return self.__webdriver.find_element(
            by=By.XPATH, value='//*[@id="mainContent"]/table/tbody/tr/td/a'
        ).get_attribute(name="href")

    def __update_progress(self, block_num, block_size, total_size) -> None:
        self.__update_frame.update_progress_bar(block_num * block_size / total_size)


if __name__ == "__main__":
    gpu = GPU()
    NvidiaWebScraper(gpu=gpu).download_installer()