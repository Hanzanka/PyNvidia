import customtkinter
import tkinter
from gpu.gpu import GPU
from ui.fonts import update_panel_font
from threading import Thread, Event, Timer


class MonitorFrame(customtkinter.CTkFrame):
    def __init__(self, master, gpu: GPU) -> None:
        super().__init__(master=master, fg_color="#0b0b0b", corner_radius=0)

        self.__gpu = gpu

        self.__util = MonitorPropertyFrame(
            master=self,
            title="Utilization",
            max_value=100,
            unit="%",
        )
        self.__util.pack(fill=tkinter.X, pady=5, ipady=5)

        self.__temp = MonitorPropertyFrame(
            master=self,
            title="Temperature",
            max_value=gpu.target_temperature,
            unit="°C",
        )
        self.__temp.pack(fill=tkinter.X, pady=5, ipady=5)

        twin_frame_1 = customtkinter.CTkFrame(
            master=self, corner_radius=0, fg_color="#0b0b0b"
        )

        self.__clock = MonitorPropertyFrame(
            master=twin_frame_1,
            title="Core Clock",
            max_value=gpu.max_graphics_clock,
            unit="MHz",
        )
        self.__clock.pack(
            fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=(0, 5), ipady=5
        )

        self.__vram = MonitorPropertyFrame(
            master=twin_frame_1,
            unit="GB",
            max_value=gpu.vram_gb,
            title="VRAM",
        )
        self.__vram.pack(
            side=tkinter.RIGHT, fill=tkinter.X, expand=True, padx=(5, 0), ipady=5
        )

        twin_frame_1.pack(fill=tkinter.X, pady=5)

        twin_frame_2 = customtkinter.CTkFrame(
            master=self, corner_radius=0, fg_color="#0b0b0b"
        )

        self.__power = MonitorPropertyFrame(
            master=twin_frame_2,
            title="Power",
            max_value=gpu.power_limit,
            unit="W",
        )
        self.__power.pack(
            side=tkinter.RIGHT, fill=tkinter.X, expand=True, padx=(5, 0), ipady=5
        )

        self.__fan = MonitorPropertyFrame(
            master=twin_frame_2, title="Fan Speed", max_value=100, unit="%"
        )
        self.__fan.pack(
            side=tkinter.RIGHT, fill=tkinter.X, expand=True, padx=(0, 5), ipady=5
        )

        twin_frame_2.pack(fill=tkinter.X, pady=5)

        timer = Timer(function=self.__update_data, interval=0.5)
        timer.daemon = True
        timer.start()

    def __update_data(self) -> None:
        try:
            data = self.__gpu.get_sensor_data()
            event = Event()
            threads = []
            
            threads.append(Thread(target=self.__util.update, args=[data["utilization"], event]))
            threads.append(Thread(target=self.__temp.update, args=[data["temperature"], event]))
            threads.append(Thread(target=self.__clock.update, args=[data["clock"], event]))
            threads.append(Thread(target=self.__vram.update, args=[data["vram_gb"], event]))
            threads.append(Thread(target=self.__power.update, args=[data["power"], event]))
            threads.append(Thread(target=self.__fan.update, args=[data["fan"], event]))
            for thread in threads:
                thread.start()
            event.set()
            for thread in threads:
                thread.join()
        except Exception as e:
            print(e)
        timer = Timer(function=self.__update_data, interval=0.5)
        timer.daemon = True
        timer.start()


class MonitorPropertyFrame(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        title: str,
        max_value: int | float,
        unit: str,
    ) -> None:
        super().__init__(master=master, corner_radius=5, fg_color="#121212")

        self.__unit = unit
        self.__max_value = max_value

        self.__label_title = customtkinter.CTkLabel(
            master=self, text=title, anchor=tkinter.S, font=update_panel_font, height=25
        )
        self.__label_title.pack(side=tkinter.TOP)

        self.__label_current = customtkinter.CTkLabel(
            master=self, text="", font=update_panel_font, width=55, height=25
        )
        self.__label_current.pack(side=tkinter.LEFT)

        self.__bar = customtkinter.CTkProgressBar(
            master=self,
            progress_color="#76b900",
            corner_radius=5,
            mode="determinate",
            fg_color="#0b0b0b",
        )
        self.__bar.set(value=0)
        self.__bar.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=5)

        self.__label_max = customtkinter.CTkLabel(
            master=self,
            text=str(max_value) + unit,
            font=update_panel_font,
            width=55,
            height=25,
        )
        self.__label_max.pack(side=tkinter.LEFT)

    def update(self, value: int | float, event: Event) -> None:
        try:
            event.wait()
            self.__label_current.configure(text=str(value) + self.__unit)
            self.__bar.set(value=value / self.__max_value)
        except Exception as e:
            print(e)
