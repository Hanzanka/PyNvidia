import subprocess


class GPU:
    def __init__(self, laptop_dev: bool = False) -> None:
        self.__laptop_dev = laptop_dev
        if laptop_dev:
            self.__series = "GeForce RTX 30 Series"
            self.__product = "GeForce RTX 3060"
            self.__type = "GeForce"
            self.__vram = 8.0
            self.__power_limit = 180
            self.__target_temperature = 100
            self.__pcie_version = 3.0
            self.__driver_version = 123.45
            self.__max_graphics_clock = 2000
            self.__max_memory_clock = 8000
            self.__full_name = "NVidia GeForce RTX 3060 12GB"
            return
        gpu_details_process = subprocess.run(
            args=[
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total,pcie.link.gen.current,power.limit,clocks.max.memory,clocks.max.graphics",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
        )
        gpu_details_output = gpu_details_process.stdout.strip().split(", ")

        self.__type = gpu_details_output[0].split(" ")[1]
        self.__series = {
            "40": "GeForce RTX 40 Series",
            "30": "GeForce RTX 30 Series",
            "20": "GeForce RTX 20 Series",
            "16": "GeForce GTX 16 Series",
            "10": "GeForce GTX 10 Series",
        }[gpu_details_output[0].split(" ")[3][0:2]]
        self.__product = gpu_details_output[0][7:]
        self.__driver_version = float(gpu_details_output[1])
        self.__vram = int(gpu_details_output[2])
        self.__power_limit = int(float(gpu_details_output[4]))
        self.__pcie_version = gpu_details_output[3]
        self.__full_name = f"{gpu_details_output[0]} {int(self.__vram / 1024)} GB"
        self.__max_memory_clock = int(gpu_details_output[5])
        self.__max_graphics_clock = int(gpu_details_output[6])

        target_temperature_process = subprocess.run(
            args=["nvidia-smi", "-q", "-d", "TEMPERATURE"],
            capture_output=True,
            text=True,
        )
        target_temperature_output = target_temperature_process.stdout.strip().split(
            "\n"
        )

        for line in target_temperature_output:
            if "GPU Target Temperature" in line:
                self.__target_temperature = int(
                    line.split(":")[1].strip().split(" ")[0]
                )

    def get_sensor_data(self) -> dict:
        if self.__laptop_dev:
            return {
                "utilization": 100,
                "vram": 6000,
                "vram_gb": 6.0,
                "temperature": 50,
                "fan": 30,
                "power": 160,
                "clock": 1690,
            }
        process = subprocess.run(
            args=[
                "nvidia-smi",
                "--query-gpu=utilization.gpu,memory.used,temperature.gpu,fan.speed,power.draw.instant,clocks.gr",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
        )
        output = process.stdout.strip().split(", ")
        
        return {
            "utilization": int(output[0]),
            "vram": int(output[1]),
            "vram_gb": round(int(output[1]) / 1024, 1),
            "temperature": int(output[2]),
            "fan": int(output[3]),
            "power": int(float(output[4])),
            "clock": int(output[5]),
        }

    @property
    def specs(self) -> tuple:
        return (
            self.__type,
            self.__series,
            self.__product,
            self.__vram,
            self.__power_limit,
            self.__target_temperature,
            self.__pcie_version,
            self.__driver_version,
            self.__max_graphics_clock,
            self.__max_memory_clock,
        )

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
        return round((self.__vram / 1024), 1)

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
        return 123.45
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
    print(gpu.get_sensor_data())
