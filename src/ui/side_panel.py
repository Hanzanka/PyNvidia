from customtkinter import CTkFrame, CTkButton, CTkLabel
import tkinter
from ui.fonts import side_panel_font


class SidePanel(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master, width=200, corner_radius=5, fg_color="#0b0b0b")
        self.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=10, pady=10)
        
        self.__home_button = CTkButton(
            master=self,
            text="Home",
            width=180,
            height=30,
            corner_radius=5,
            fg_color="#76b900",
            text_color="#000000",
            font=side_panel_font,
            hover_color="#91c733",
        )
        self.__home_button.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.__settings_button = CTkButton(
            master=self,
            text="Settings",
            width=180,
            height=30,
            corner_radius=5,
            fg_color="#76b900",
            text_color="#000000",
            font=side_panel_font,
            hover_color="#91c733",
        )
        self.__settings_button.grid(row=1, column=0, padx=10, pady=5)

        self.__credit_label = CTkLabel(
            master=self,
            text="Made By Ville Einiö\ngithub.com/Hanzanka",
            width=180,
            height=30,
            anchor="s",
            font=side_panel_font,
        )
        self.__credit_label.grid(row=2, column=0, padx=10, pady=10, sticky=tkinter.S)
        
        self.rowconfigure(index=2, weight=1)
