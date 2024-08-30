"""
Module for handle commands and arguments
"""
import sys
from importlib import import_module

from typing_extensions import Any

from .commands import BaseCommand


class CommandLineManager:
    def __init__(self, args: list):
        self.args = args

    def __import_class(self, class_path: str, class_name: str) -> BaseCommand:
        """Method for dynamic class import"""
        return getattr(import_module(class_path), class_name)()

    def parse_args_to_command(self) -> dict[str, str | dict[str, str] | BaseCommand] | None:
        """Method for parse args to command"""
        command: str = self.args[0]
        args: list[str] = self.args[1:]
        command_args: dict[str, Any] = {}

        command_class = self.__import_class(
            f"test_framework.core.management.commands.{command}",
            f"{command.capitalize()}Command"
        )

        if len(args) == 0:
            sys.stdout.write(f"Requires arguments: {str(command_class.requires)}")

            return

        params: list[str] = args[::2]
        values: list[str] = args[1::2]

        for param in params:
            if param.replace("--", "") not in command_class.requires:
                sys.stdout.write(f"Required params: {command_class.requires}")

                return

        if len(params) != len(values):
            sys.stdout.write("Something wrong in params, check and try again.")

            return

        for i in range(len(params)):
            command_args[params[i].replace("--", "")] = values[i]

        return {
            "command": command,
            "class": command_class,
            "args": command_args
        }

    def execute(self):
        """Command line manager executor"""
        if len(self.args) == 0 or self.args[0] == "help":
            sys.stdout.write("help")
        else:
            if (command := self.parse_args_to_command()) is None:
                sys.stdout.write("Found problems")
            else:
                command['class'].handle(**command["args"])


def command_line_handler():
    """Entrypoint"""
    print(sys.argv)
    CommandLineManager(args=sys.argv[1:]).execute()
