import customtkinter
import tkinter
from gpu.gpu import GPU
from ui.update_frame import UpdateFrame
from scraper.scraper import NvidiaWebScraper


class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, driver_downloader: NvidiaWebScraper) -> None:
        super().__init__(master=master, corner_radius=5, fg_color="#0b0b0b")

        self.pack(
            fill=tkinter.BOTH, padx=(0, 10), pady=10, expand=True, side=tkinter.RIGHT
        )

        title_font = customtkinter.CTkFont(family="Fira Code", weight="bold", size=30)

        gpu = GPU()

        title = customtkinter.CTkLabel(
            master=self,
            text=f"NVidia {gpu.product} {gpu.vram}",
            font=title_font,
            padx=10,
            pady=10,
            corner_radius=5,
        )

        title.pack()
        UpdateFrame(master=self, driver_downloader=driver_downloader)
