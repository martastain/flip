from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from flip.config import FlipConfig
from flip.console import Response
from flip.flipper import Flipper
from flip.consts import FlipperCommands

# build word completer from FlipperCommands enum
flipper_commands = WordCompleter(
    [command.value for command in FlipperCommands],
    ignore_case=True,
)


class Flip:
    def __init__(self):
        self.config = FlipConfig()

        Response.splash()

        self.prompt_session = PromptSession()
        self.flipper = Flipper(com=self.config.tty)

    @property
    def prompt_string(self) -> str:
        template = "{hardware_name}@{firmware_version}: {pwd}\n$ "

        return template.format(
            hardware_name=self.flipper.device_info.hardware_name.lower(),
            firmware_version=self.flipper.device_info.firmware_version.lower(),
            pwd=self.flipper.pwd,
        )

    def prompt(self):
        text = self.prompt_session.prompt(
            self.prompt_string,
            # completer=flipper_commands,
            # complete_while_typing=True,
        )

        match text:
            case "exit":
                raise KeyboardInterrupt
            case "connect":
                self.flipper.connect()
            case "vibr":
                self.flipper.vibro_alert()
            case _:
                if (res := self.flipper.query(text)) is not None:
                    print(res)
                    print()


def main():
    flip = Flip()
    while True:
        try:
            flip.prompt()
        except KeyboardInterrupt:
            print()
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
