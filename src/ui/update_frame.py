import customtkinter
import tkinter
from scraper.scraper import NvidiaWebScraper
from threading import Lock, Thread
from time import sleep
from utils.utils import extract_files, install_driver, get_path
from ui.fonts import update_panel_font
import os


class UpdateFrame(customtkinter.CTkFrame):
    def __init__(self, master, driver_downloader: NvidiaWebScraper) -> None:
        super().__init__(master=master, fg_color="#0b0b0b")
        self.pack(fill=tkinter.X, side=tkinter.BOTTOM, padx=10, pady=10)

        self.__driver_downloader = driver_downloader

        self.__check_for_updates_button = customtkinter.CTkButton(
            master=self,
            corner_radius=5,
            fg_color="#76b900",
            text_color="#000000",
            text="Check For Update",
            font=update_panel_font,
            hover_color="#91c733",
            text_color_disabled="#000000",
        )
        self.__check_for_updates_button.configure(
            command=self.__check_update_button_click
        )
        self.__check_for_updates_button.pack(
            side=tkinter.RIGHT, anchor=tkinter.SE, padx=(10, 0)
        )

        self.__infoframe = customtkinter.CTkFrame(master=self, fg_color="#0b0b0b")

        self.__update_label = customtkinter.CTkLabel(
            master=self.__infoframe, corner_radius=5, font=update_panel_font
        )
        self.__update_label.pack(anchor=tkinter.W, side=tkinter.TOP)

        self.__download_bar = customtkinter.CTkProgressBar(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#0b0b0b",
            progress_color="#76b900",
            bg_color="#0b0b0b",
            mode="indeterminate",
        )
        self.__download_bar.set(0)
        self.__download_bar.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)

        self.__download_button = customtkinter.CTkButton(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#76b900",
            text_color="#000000",
            text="Download Update",
            font=update_panel_font,
            command=self.__download_button_click,
            hover_color="#91c733",
        )

        self.__install_button = customtkinter.CTkButton(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#76b900",
            text_color="#000000",
            text="Install Update",
            font=update_panel_font,
            command=self.__install_button_click,
            hover_color="#91c733",
        )

        self.__update_lock = Lock()

        self.__downloaded_driver_version = None
        self.__download_path = get_path("download")

    def __check_update_button_click(self) -> None:
        self.__check_for_updates_button.configure(state="disabled", fg_color="#395b00")
        Thread(target=self.__check_for_updates).start()

    def __download_button_click(self) -> None:
        Thread(target=self.__download_update).start()

    def __install_button_click(self) -> None:
        Thread(target=self.__install_driver).start()

    def __check_for_updates(self) -> None:
        self.__update_label.configure(text="Checking For Updates")
        self.__download_bar.start()
        self.__infoframe.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)

        update_available, driver_version = self.__driver_downloader.check_for_updates()

        if not update_available:
            self.__update_label.configure(text="No Updates Available")
            self.__download_bar.pack_forget()
            return

        self.__download_bar.stop()
        self.__download_bar.pack_forget()
        self.__downloaded_driver_version = driver_version

        if os.path.isdir(f"{self.__download_path}{driver_version}"):
            self.__update_label.configure(text="Driver Ready To Be Installed")
            self.__install_button.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)
            return

        self.__download_button.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)
        self.__update_label.configure(
            text=f"Driver Version {driver_version} Is Available"
        )

    def __download_update(self) -> None:
        self.__download_button.pack_forget()
        self.__update_label.configure(text="Downloading Installer")
        self.__download_bar.configure(mode="determinate")
        self.__download_bar.set(0)
        self.__download_bar.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)
        self.__driver_downloader.download_installer(reporthook=self.__update_progress)
        self.__update_label.configure(text="Extracting Files")
        self.__download_bar.configure(mode="indeterminate")
        self.__download_bar.start()
        extract_files()
        self.__download_bar.stop()
        self.__download_bar.pack_forget()
        self.__update_label.configure(text="Driver Ready To Be Installed")
        self.__install_button.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)

    def __install_driver(self) -> None:
        self.__install_button.pack_forget()
        self.__update_label.configure(text="Installing Driver")
        self.__download_bar.configure(mode="indeterminate")
        self.__download_bar.start()
        install_driver(driver_version=self.__downloaded_driver_version)

    def __update_progress_label(self, size, total_size) -> None:
        self.__update_label.configure(
            text=f"Downloading Installer {size:.1f} MB / {total_size:.1f} MB"
        )

    def __set_bar_progress(self, value) -> None:
        self.__download_bar.set(value=value)
        sleep(0.75)
        self.__update_lock.release()

    def __update_progress(self, block_num, block_size, total_size) -> None:
        if self.__update_lock.acquire(blocking=False):
            value = block_num * block_size / total_size
            Thread(target=self.__set_bar_progress, args=[value]).start()
            Thread(
                target=self.__update_progress_label,
                args=[block_num * block_size / 1024**2, total_size / 1024**2],
            ).start()
        elif block_num * block_size >= total_size:
            self.__download_bar.set(1)
            self.__update_label.configure(text="Finishing Download")
