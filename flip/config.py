from pydantic import Field
from pydantic_settings import BaseSettings


class FlipConfig(BaseSettings):
    class Config:
        env_prefix = "FLIP_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    prompt: str = Field("{device_name}$ ", env="PROMPT")
    tty: str = Field("/dev/ttyACM0", env="TTY")
