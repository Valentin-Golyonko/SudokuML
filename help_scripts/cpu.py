"""
pip install psutil

sudo apt-get install nvidia-utils-<version>

sudo apt-get install lm-sensors
pip install pandas
pip install pyarrow
"""

import io
import subprocess

import pandas as pd


def get_cpu_temperature_linux():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temperature_str = file.read()

    temperature_celsius = int(temperature_str) / 1000
    return temperature_celsius


def get_cpu_fan_speed():
    cpu_fan_speed = None
    gpu_fan_speed = None

    try:
        command_output = subprocess.check_output(["sensors", "-u"], text=True)
        sensor_data = pd.read_csv(
            io.StringIO(command_output),
            delimiter=":",
            header=None,
            skiprows=[0, 1, 2],
        )

        for index, row in sensor_data.iterrows():
            if cpu_fan_speed is not None and gpu_fan_speed is not None:
                break

            if "fan1_input" in row[0].lower():
                cpu_fan_speed = float(row[1])
            if "fan2_input" in row[0].lower():
                gpu_fan_speed = float(row[1])

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    return cpu_fan_speed, gpu_fan_speed


def get_gpu_temperature():
    try:
        command_output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu",
                "--format=csv,noheader,nounits",
            ]
        )
        temperature_str = command_output.decode("utf-8").strip()
        temperature_celsius = int(temperature_str)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    return temperature_celsius


if __name__ == "__main__":
    temperature = get_cpu_temperature_linux()
    print(f"CPU Temperature: {temperature} °C")

    cpu_fan, gpu_fan = get_cpu_fan_speed()
    print(f"CPU Fan Speed: {cpu_fan} RPM")
    print(f"GPU Fan Speed: {gpu_fan} RPM")

    temperature = get_gpu_temperature()
    print(f"GPU Temperature: {temperature} °C")
