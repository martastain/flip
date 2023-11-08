from pydantic import BaseModel


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

