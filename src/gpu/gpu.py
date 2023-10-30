import subprocess


class GPU:
    def __init__(self) -> None:
        gpu_details_process = subprocess.run(
            args=[
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total,pcie.link.gen.current,power.limit",
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
        self.__vram = int(int(gpu_details_output[2]) / 1024)
        self.__power_limit = int(float(gpu_details_output[4]))
        self.__pcie_version = gpu_details_output[3]
        self.__full_name = f"{gpu_details_output[0]} {self.__vram} GB"

        max_clocks_process = subprocess.run(
            args=["nvidia-smi", "-q", "-d", "CLOCK"], capture_output=True, text=True
        )
        max_clocks_output = max_clocks_process.stdout.strip().split("\n")
        
        for line in max_clocks_output:
            if "Max Clocks" in line:
                self.__max_graphics_clock = int(
                    max_clocks_output[max_clocks_output.index(line) + 1]
                    .split(":")[1]
                    .strip()
                    .split(" ")[0]
                )
                self.__max_memory_clock = int(
                    max_clocks_output[max_clocks_output.index(line) + 3]
                    .split(":")[1]
                    .strip()
                    .split(" ")[0]
                )

    @property
    def specs(self) -> tuple:
        return (
            self.__type,
            self.__series,
            self.__product,
            self.__vram,
            self.__power_limit,
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
    def vram(self) -> int:
        return self.__vram

    @property
    def power_limit(self) -> int:
        return self.__power_limit

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
    print("PCIe version:", gpu.pcie_version)
    print("Driver version:", gpu.driver_version)
    print("Full name:", gpu.full_name)
