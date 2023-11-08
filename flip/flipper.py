import os
import serial
import time

from typing import Any

from flip.console import Response
from flip.models import DeviceInfo, PowerInfo


class Filesystem:
    def __init__(self, parent: "Flipper"):
        self.parent = parent
        self.pwd = "/ext"

    @property
    def commands(self):
        return {
            "ls": self.ls,
            "dir": self.ls,
            "cd": self.cd,
            "cat": self.cat,
        }

    def ls(self) -> str:
        return self.parent.query(f"storage list {self.pwd}")

    def cd(self, path: str) -> None:
        if path.startswith("/"):
            new_path = path
        else:
            new_path = os.path.join(
                self.pwd,
                path,
            )
        new_path = os.path.normpath(new_path)

        r = self.parent.query(f"storage stat {new_path}")
        if r.split(",")[0] not in ["Directory", "Storage"]:
            Response.error(f"{new_path} is not a directory")
            print(r)
        self.pwd = new_path

    def cat(self, path: str) -> str:
        cat_path = os.path.join(self.pwd, path)
        cat_path = os.path.normpath(cat_path)

        r = self.parent.query(f"storage stat {cat_path}")
        if r.split(",")[0] != "File":
            Response.error(f"{cat_path} is not a file")
            print(r)

        print(self.parent.query(f"storage read {cat_path}"))


class Flipper:
    def __init__(self, com: str) -> None:
        self.com = com
        self.connection = None
        self.filesystem = Filesystem(self)
        self.connect(timeout=1)

    @property
    def pwd(self) -> str:
        return self.filesystem.pwd

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

    def query(self, command: str) -> str | None:
        if self.connection is None:
            Response.error("Not connected")
            return ""

        carg = command.split(" ", 1)
        if carg[0] in self.filesystem.commands:
            if len(carg) == 1:
                return self.filesystem.commands[carg[0]]()
            return self.filesystem.commands[carg[0]](carg[1])

        self.connection.write(f"{command}\r".encode())
        self.connection.readline()
        reply = self.connection.read_until(b">:").decode().rstrip(">:\r\n")

        return reply or None

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
