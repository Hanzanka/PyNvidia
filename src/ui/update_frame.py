import customtkinter
import tkinter
from scraper.scraper import NvidiaWebScraper
from threading import Lock, Thread
from time import sleep
import subprocess
import os
from pathlib import Path


class UpdateFrame(customtkinter.CTkFrame):
    def __init__(self, master, driver_downloader: NvidiaWebScraper) -> None:
        super().__init__(master=master, fg_color="#0b0b0b")
        self.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        self.__driver_downloader = driver_downloader

        font = customtkinter.CTkFont(family="Fira Code", weight="bold", size=12)

        self.__check_for_update = customtkinter.CTkButton(
            master=self,
            corner_radius=5,
            fg_color="#91c733",
            text_color="#000000",
            text="Check For Update",
            font=font,
        )
        self.__check_for_update.configure(command=self.__check_update_button_click)
        self.__check_for_update.pack(
            side=tkinter.RIGHT, anchor=tkinter.SE, padx=10, pady=10
        )

        self.__infoframe = customtkinter.CTkFrame(master=self, fg_color="#0b0b0b")

        self.__update_label = customtkinter.CTkLabel(
            master=self.__infoframe, corner_radius=5, font=font
        )
        self.__update_label.pack(padx=5, pady=0, anchor=tkinter.W, side=tkinter.TOP)

        self.__download_bar = customtkinter.CTkProgressBar(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#0b0b0b",
            progress_color="#91c733",
            bg_color="#0b0b0b",
            mode="indeterminate",
        )
        self.__download_bar.set(0)
        self.__download_bar.pack(
            padx=10, pady=(0, 10), expand=True, fill=tkinter.X, side=tkinter.LEFT
        )

        self.__download_button = customtkinter.CTkButton(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#91c733",
            text_color="#000000",
            text="Download Update",
            font=font,
            command=self.__download_button_click,
        )

        self.__install_button = customtkinter.CTkButton(
            master=self.__infoframe,
            corner_radius=5,
            fg_color="#91c733",
            text_color="#000000",
            text="Install Update",
            font=font,
            command=self.__install_button_click,
        )

        self.__update_lock = Lock()

    def __check_update_button_click(self) -> None:
        Thread(target=self.__check_for_updates).start()

    def __download_button_click(self) -> None:
        Thread(target=self.__download_update).start()

    def __install_button_click(self) -> None:
        Thread(target=self.__install_driver).start()

    def __check_for_updates(self) -> None:
        self.__update_label.configure(text="Checking For Updates")
        self.__download_bar.start()
        self.__infoframe.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)

        update_available = self.__driver_downloader.check_for_updates
        sleep(2)

        if update_available:
            self.__download_bar.stop()
            self.__download_bar.pack_forget()
            self.__download_button.pack(
                padx=10, pady=(0, 10), expand=True, fill=tkinter.X, side=tkinter.LEFT
            )
            self.__update_label.configure(text="Update Available")
        else:
            self.__update_label.configure(text="No Updates Available")
            self.__download_bar.pack_forget()

    def __download_update(self) -> None:
        self.__download_button.pack_forget()
        self.__update_label.configure(text="Downloading Installer")
        self.__download_bar.configure(mode="determinate")
        self.__download_bar.set(0)
        self.__download_bar.pack(
            padx=10, pady=(0, 10), expand=True, fill=tkinter.X, side=tkinter.LEFT
        )
        self.__driver_downloader.download_installer(
            reporthook=self.__update_progress_bar
        )
        self.__update_label.configure(text="Download Complete")
        self.__download_bar.pack_forget()
        self.__install_button.pack(
            padx=10, pady=(0, 10), expand=True, fill=tkinter.X, side=tkinter.LEFT
        )

    def __install_driver(self) -> None:
        pass

    def __set_bar_progress(self, value) -> None:
        self.__download_bar.set(value=value)
        sleep(0.5)
        self.__update_lock.release()

    def __update_progress_bar(self, block_num, block_size, total_size) -> None:
        if self.__update_lock.acquire(blocking=False):
            value = block_num * block_size / total_size
            Thread(target=self.__set_bar_progress, args=[value]).start()
