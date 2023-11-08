from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

import os
import platform

def clear_screen():
    # Check if the operating system is Windows
    if platform.system().lower() == "windows":
        os.system('cls')  # Clear screen command for Windows
    else:
        os.system('clear')  # Clear screen command for Unix/Linux/macOS

class Response:
    @classmethod
    def print_formatted(cls, tokens: list[tuple[str, str]]):
        text = FormattedText(tokens)
        print_formatted_text(text)

    @classmethod
    def error(cls, message: str) -> None:
        cls.print_formatted(
            [
                ("#ff0000", "Error: "),
                ("", message),
            ]
        )

    @classmethod
    def success(cls, message: str) -> None:
        cls.print_formatted(
            [
                ("#00ff00", "Success: "),
                ("", message),
            ]
        )

    def splash() -> None:
        clear_screen()
