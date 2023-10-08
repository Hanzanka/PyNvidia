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


if __name__ == "__main__":
    extract_files()
