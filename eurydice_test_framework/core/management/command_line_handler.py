"""
Module for handle commands and arguments
"""
from importlib import import_module
from sys import argv, stdout
from typing import Any

HELP = (
    "Hi. Welcome to the Eurydice.\n\n"
    "It's framework for fast build automation testing environment.\n"
    "Available commands:\n"
    "\tproject\n"
    "\t\tinit --project-name [PROJECT_NAME] — build project directory structure.\n"
    "\tservice\n"
    "\t\tadd --project-name [PROJECT_NAME] --service-name [SERVICE_NAME] — add service for testing to the project.\n"
    # "\t\tremove --project-name [PROJECT_NAME] --service-name [SERVICE_NAME] —  remove service from specific project.\n"
    "\tdatabase\n"
    "\t\tinit --user [USER] --password [PASSWORD] --database [DATABASE] — add .env and docker-compose files for "
    "build pgsql database\n"
)


class CommandLineManager:
    def __init__(self, args: list):
        self.args = args

    def __import_class(self, class_path: str, class_name: str):
        """Method for dynamic class import"""
        return getattr(import_module(class_path), class_name)()

    def parse_args_to_command(self) -> dict[str, str | dict[str, str] | Any] | None:
        """Method for parse args to command"""
        try:
            group_name = self.args[0]
            action_name = self.args[1]
            kw_arguments = self.args[1:]

            group_class = self.__import_class(
                f"eurydice_test_framework.core.management.command_groups.{group_name}",
                f"{group_name.capitalize()}CommandGroup"
            )

            props: list[str] = [el for el in kw_arguments if "--" in el]
            params: list[str] = [el for el in kw_arguments[1:] if "--" not in el]

            if len(props) != len(params):
                stdout.write(f"{action_name} need only {group_class.requires[action_name]}\n")

                return None
            else:
                args: dict[str, str] = {}
                for i, _ in enumerate(props):
                    args[props[i].replace("--", "").replace("-", "_")] = params[i]

                return {
                    "action": action_name,
                    "group": group_class,
                    "args": args
                }
        except Exception as e:
            stdout.write(HELP)

    def execute(self):
        """Command line manager executor"""
        if len(self.args) == 0 or self.args[0] == "help":
            stdout.write(HELP)
        else:
            if (command := self.parse_args_to_command()) is None:
                stdout.write("Found problems")
            else:
                getattr(command['group'], f"{command['action']}_action")(**command["args"])


def command_line_handler():
    """Entrypoint"""
    CommandLineManager(args=argv[1:]).execute()
