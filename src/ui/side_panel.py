from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkFont
import tkinter


class SidePanel(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(
            master=master, width=200, corner_radius=5, fg_color="#0b0b0b"
        )
        self.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=10, pady=10)
        self.__add_components()

    def __add_components(self) -> None:
        font = CTkFont(family="Fira Code", weight="bold", size=14)
        home_button = CTkButton(
            master=self,
            text="Home",
            width=180,
            height=30,
            corner_radius=5,
            fg_color="#91c733",
            text_color="#000000",
            font=font,
        )
        settings_button = CTkButton(
            master=self,
            text="Settings",
            width=180,
            height=30,
            corner_radius=5,
            fg_color="#91c733",
            text_color="#000000",
            font=font,
        )
        credit_label = CTkLabel(
            master=self,
            text="Made By Ville Einiö\ngithub.com/Hanzanka",
            width=180,
            height=30,
            anchor="s",
            font=font,
        )

        home_button.grid(row=0, column=0, padx=10, pady=(10, 0))
        settings_button.grid(row=1, column=0, padx=10, pady=5)
        credit_label.grid(row=2, column=0, padx=10, pady=10, sticky=tkinter.S)
        self.rowconfigure(index=2, weight=1)
