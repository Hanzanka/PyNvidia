import pynvml


class GPU:
    def __init__(self) -> None:
        pynvml.nvmlInit()
        self.__gpu = pynvml.nvmlDeviceGetHandleByIndex(0)

        self.__name = pynvml.nvmlDeviceGetName(self.__gpu)
        self.__type = self.__name.split(" ")[1]
        self.__series = {
            "40": "GeForce RTX 40 Series",
            "30": "GeForce RTX 30 Series",
            "20": "GeForce RTX 20 Series",
            "16": "GeForce GTX 16 Series",
            "10": "GeForce GTX 10 Series",
        }[self.__name.split(" ")[3][0:2]]
        self.__product = self.__name[7:]
        self.__driver_version = float(pynvml.nvmlSystemGetDriverVersion())
        self.__vram = pynvml.nvmlDeviceGetMemoryInfo(self.__gpu).total
        self.__power_limit = int(
            round((pynvml.nvmlDeviceGetPowerManagementLimit(self.__gpu) / 10**3), 0)
        )
        self.__pcie_version = pynvml.nvmlDeviceGetCurrPcieLinkGeneration(self.__gpu)
        self.__full_name = f"{self.__name} {int(self.__vram / 1024**3)} GB"
        self.__max_memory_clock = pynvml.nvmlDeviceGetMaxClockInfo(
            self.__gpu, pynvml.NVML_CLOCK_MEM
        )
        self.__max_graphics_clock = pynvml.nvmlDeviceGetMaxClockInfo(
            self.__gpu, pynvml.NVML_CLOCK_GRAPHICS
        )
        self.__target_temperature = pynvml.nvmlDeviceGetTemperatureThreshold(
            self.__gpu, pynvml.NVML_TEMPERATURE_THRESHOLD_ACOUSTIC_MAX
        )

    def shutdown_nvml(self) -> None:
        pynvml.nvmlShutdown()

    def get_sensor_data(self) -> dict:
        utilization = pynvml.nvmlDeviceGetUtilizationRates(self.__gpu).gpu
        vram = pynvml.nvmlDeviceGetMemoryInfo(self.__gpu).used
        temperature = pynvml.nvmlDeviceGetTemperature(
            self.__gpu, pynvml.NVML_TEMPERATURE_GPU
        )
        fan = pynvml.nvmlDeviceGetFanSpeed(self.__gpu)
        power_usage = int(
            round((pynvml.nvmlDeviceGetPowerUsage(self.__gpu) / 10**3), 0)
        )
        clock = pynvml.nvmlDeviceGetClockInfo(self.__gpu, pynvml.NVML_CLOCK_GRAPHICS)
        return {
            "utilization": utilization,
            "vram": vram,
            "vram_gb": round((vram / 1024**3), 1),
            "temperature": temperature,
            "fan": fan,
            "power": power_usage,
            "clock": clock,
        }

    @property
    def type(self) -> str:
        return self.__type

    @property
    def series(self) -> str:
        return self.__series

    @property
    def product(self) -> str:
        return self.__product

    @property
    def max_graphics_clock(self) -> int:
        return self.__max_graphics_clock

    @property
    def max_memory_clock(self) -> int:
        return self.__max_memory_clock

    @property
    def vram_gb(self) -> float:
        return round((self.__vram / 1024**3), 1)

    @property
    def vram(self) -> int:
        return self.__vram

    @property
    def power_limit(self) -> int:
        return self.__power_limit

    @property
    def target_temperature(self) -> int:
        return self.__target_temperature

    @property
    def pcie_version(self) -> int:
        return self.__pcie_version

    @property
    def driver_version(self) -> float:
        return self.__driver_version

    @property
    def full_name(self) -> str:
        return self.__full_name


if __name__ == "__main__":
    gpu = GPU()
    print("Type:", gpu.type)
    print("Series:", gpu.series)
    print("Product:", gpu.product)
    print("Max graphics clock:", gpu.max_graphics_clock)
    print("Max memory clock:", gpu.max_memory_clock)
    print("VRAM:", gpu.vram)
    print("Power limit:", gpu.power_limit)
    print("Target temperature:", gpu.target_temperature)
    print("PCIe version:", gpu.pcie_version)
    print("Driver version:", gpu.driver_version)
    print("Full name:", gpu.full_name)
    print("Max Mem Clock:", gpu.max_memory_clock)
    print("Max Core Clock:", gpu.max_graphics_clock)
    print(gpu.get_sensor_data())
    gpu.shutdown_nvml()
