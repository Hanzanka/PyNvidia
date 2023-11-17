import customtkinter
import tkinter
from gpu.gpu import GPU
from ui.update_frame import UpdateFrame
from scraper.scraper import NvidiaWebScraper
from ui.fonts import title_font
from ui.monitor_frame import MonitorFrame


class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, driver_downloader: NvidiaWebScraper) -> None:
        super().__init__(master=master, corner_radius=5, fg_color="#0b0b0b")

        gpu = GPU()

        title = customtkinter.CTkLabel(
            master=self,
            text=gpu.full_name,
            font=title_font,
            padx=10,
            pady=10,
            corner_radius=5,
        )
        title.pack()

        self.__update_frame = UpdateFrame(
            master=self, driver_downloader=driver_downloader
        )
        self.__update_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM, padx=10, pady=(5, 10))

        self.__monitor_frame = MonitorFrame(master=self, gpu=gpu)
        self.__monitor_frame.pack(fill=tkinter.BOTH, side=tkinter.BOTTOM, padx=10)
