from customtkinter import CTk
import customtkinter
from ui.side_panel import SidePanel
from tkinter import *
from ui.home_frame import HomeFrame
from scraper.scraper import NvidiaWebScraper


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class App(CTk):
    def __init__(self, driver_downloader: NvidiaWebScraper):
        super().__init__(fg_color="#050505")
        self.geometry("900x500")
        self.title("Nvidia Driver Installer")
        SidePanel(master=self)
        self.__home_panel = HomeFrame(self, driver_downloader=driver_downloader)
