
# PyNvidia
This repository provides a comprehensive solution for managing NVIDIA GPU drivers. It includes a utility for updating NVIDIA GPU drivers to their latest versions via easy to use user-interface.

In addition, it features a monitoring system that keeps track of the state of your NVIDIA GPU. This includes monitoring GPU temperature, memory usage, clock speed, and more. Please note that the monitoring is currently real-time only and does not support logging or retrieving past data.

## Features
- Driver Updates: Automatically updates NVIDIA GPU drivers to the latest version.
- GPU Monitoring: Real-time monitoring of GPU state.

## UI
### Home Screen
- Driver Updates: Automatically update your with a few clicks.
- GPU Monitoring: Display GPU statistics in real-time.

![Home Screen](https://github.com/Hanzanka/PyNvidia/blob/main/homescreen.png?raw=true)

## Dependencies
- [CustomTkinter](https://github.com/tomschimansky/customtkinter)
- Tkinter
- [Selenium](https://pypi.org/project/selenium/)
- [pyuac](https://pypi.org/project/pyuac/)
- [Fira Code](https://fonts.google.com/specimen/Fira+Code)(Probably will be changed or to be automatically installed with the program)


## Installation
The repository is in early development, so the program wouldn't work by directly cloning the repository. However if you still want to get it work, here is the steps to get it work:

1. Clone the repository
```bash
git clone https://github.com/Hanzanka/PyNvidia.git
```
2. Create a config.json -file to `src/`

3. Add these lines to config.json:
```json
{
    "paths": {
        "program": "(path to where the repository cloned)",
        "download": "(path to where the driver files are downloaded)"
    }
}
```
