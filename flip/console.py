from prompt_toolkit import print_formatted_text


class Response:
    @classmethod
    def error(cls, message: str) -> None:
        print_formatted_text([
            ("#ff0000", "Error: "),
            ("", message),
        ])


    @classmethod
    def success(cls, message: str) -> None:
        print_formatted_text([
            ("#00ff00", "Success: "),
            ("", message),
        ])

    def splash() -> None:
        return
