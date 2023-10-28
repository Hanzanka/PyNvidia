class CouldNotLocate7zipKey(Exception):
    pass


class CouldNotLocate7zipKeyValue(Exception):
    pass


def locate_7zip() -> str:
    from winreg import HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
    import json
    import pathlib

    config_path = str(pathlib.Path(__file__).parents[1]) + "/config.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    try:
        with OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip") as key:
            try:
                config["paths"]["sevenz_path"] = (
                    QueryValueEx(key, "Path")[0].replace("\\", "/") + "7z.exe"
                )
            except FileNotFoundError:
                raise CouldNotLocate7zipKeyValue(
                    "Could not locate 7-zip installation (Path not found in registry key)"
                )
    except FileNotFoundError:
        raise CouldNotLocate7zipKey(
            "Could not locate 7-zip installation (Key not found in registry)"
        )
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)


def extract_files() -> None:
    from options.options import download_path, sevenz_path
    import os
    import subprocess

    folder_path = download_path + str(
        max([float(os.path.splitext(file)[0]) for file in os.listdir(download_path)])
    )
    driver_path = folder_path + ".exe"

    subprocess.run(
        args=[
            sevenz_path,
            "x",
            driver_path,
            "-aoa",
            "-bso0",
            "-bsp0",
            f"-o{folder_path}",
        ]
    )
    os.remove(driver_path)


def install_driver(driver_path: str) -> None:
    import subprocess

    try:
        subprocess.Popen(args=[driver_path])
    except Exception:
        pass


if __name__ == "__main__":
    locate_7zip()
