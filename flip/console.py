from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


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
        return
