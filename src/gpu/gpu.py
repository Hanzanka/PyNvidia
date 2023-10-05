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
        output = gpu_details_process.stdout.strip()

        self.__type = output.split(", ")[0].split(" ")[1]

        self.__series = {
            "40": "GeForce RTX 40 Series",
            "30": "GeForce RTX 30 Series",
            "20": "GeForce RTX 20 Series",
            "16": "GeForce GTX 16 Series",
            "10": "GeForce GTX 10 Series",
        }[output.split(", ")[0].split(" ")[3][0:2]]

        self.__product = output.split(", ")[0][7:]

        self.__driver_version = output.split(", ")[1]

        self.__vram = str(int(int(output.split(", ")[2]) / 1024)) + " GB"

        self.__power_limit = output.split(", ")[3]

    @property
    def specs(self) -> tuple:
        return (
            self.__type,
            self.__series,
            self.__product,
            self.__vram,
            self.__power_limit,
            self.__driver_version,
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
    def vram(self) -> str:
        return self.__vram

    @property
    def power_limit(self) -> str:
        return self.__power_limit

    @property
    def driver_version(self) -> str:
        return self.__driver_version


if __name__ == "__main__":
    print(GPU().specs)
