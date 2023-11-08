import serial
import threading
import time

from pydantic import BaseModel

from typing import Any


from flip.console import Response


class DeviceInfo(BaseModel):
    hardware_model: str
    hardware_name: str
    hardware_ver: int
    firmware_version: str
    firmware_origin_fork: str
    firmware_origin_git: str


class PowerInfo(BaseModel):
    charge_level: int
    charge_state: str
    battery_temp: int
    battery_health: int


class Flipper:
    def __init__(self, com: str) -> None:
        self.com = com
        self.connection = None
        self.connect(timeout=1)
        self.current_directory = "/ext"

    def connect(self, timeout=10) -> None:
        try:
            self.connection = serial.Serial(
                port=self.com,
                baudrate=9600,
                bytesize=8,
                timeout=timeout,
                stopbits=serial.STOPBITS_ONE,
            )
        except KeyboardInterrupt:
            Response.error("Connection aborted!")
        except Exception:
            Response.error(f"Could not connect to {self.com}")

        else:
            # skip welcome banner
            self.connection.read_until(b">:")

        # self.vibro_alert()

    def query(self, command: str) -> str:
        if self.connection is None:
            Response.error("Not connected")
            return ""

        if command == "ls":
            return self.ls()
        elif command.startswith("cd"):
            self.cd(command.split(" ", 1)[1])
            return ""

        self.connection.write(f"{command}\r".encode())
        self.connection.readline()
        reply = self.connection.read_until(b">:").decode().rstrip(">:\r\n")
        return reply

    def ls(self) -> str:
        return self.query(f"storage list {self.current_directory}")

    def cd(self, directory: str) -> None:
        if directory == "..":
            self.current_directory = "/".join(self.current_directory.split("/")[:-1])
        elif directory.startswith("/"):
            self.current_directory = directory
        else:
            self.current_directory = f"{self.current_directory}/{directory}"

    def ctrl_c(self):
        self.connection.write(b"\x03")

    def parse_info(self, raw_info: str) -> dict[str, Any]:
        info = {}
        for row in raw_info.split("\n"):
            kv = row.split(":", 1)
            if len(kv) != 2:
                continue
            key = kv[0].strip().replace(".", "_")
            value = kv[1].strip()

            value = value.strip()
            if value.isdigit():
                value = int(value)
            elif value == "true":
                value = True
            elif value == "false":
                value = False
            elif value.endswith("K") and value.strip("K").isdigit():
                value = int(value.strip("K")) * 1024
            info[key] = value
        return info

    @property
    def device_info(self) -> DeviceInfo | None:
        if self.connection is None:
            return None
        if not hasattr(self, "_device_info") or self._device_info is None:
            res = self.query("info device")
            self._device_info = DeviceInfo(**self.parse_info(res))
        return self._device_info

    @property
    def power_info(self) -> PowerInfo | None:
        if self.connection is None:
            return None
        res = self.query("info power")
        info = self.parse_info(res)
        return PowerInfo(**info)

    def vibro_alert(self):
        def alert_thread():
            self.query("vibro 1")
            time.sleep(0.2)
            self.query("vibro 0")
            time.sleep(0.1)
            self.query("vibro 1")
            time.sleep(0.2)
            self.query("vibro 0")

        alert_thread()
