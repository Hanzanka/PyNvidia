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
                config["paths"]["sevenz"] = (
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


def get_path(key: str) -> str:
    import json
    import pathlib

    with open(
        str(pathlib.Path(__file__).parents[1]) + "/config.json", "r"
    ) as config_file:
        return json.load(config_file)["paths"][key]
