import sys

from eurydice_test_ramework.core.management.commands import BaseCommand
from eurydice_test_ramework.core.management.directory_handler import DirectoryHandler


class InitCommand(BaseCommand):
    """Init command: build directory structure"""
    help = (
        "It's command init project and creates directory structure"
    )
    command = "init"
    requires = ["project_name"]

    def handle(self, project_name: str):
        """Handler Init command: create directory structure

        Directory structure example:
        | tests
          | service_1
          | service_2
        | api
          | service_1
          | service_2
        | test_data
        """

        DirectoryHandler().create_dir(project_name)
        DirectoryHandler().create_dir(f"{project_name}/tests")
        DirectoryHandler().create_dir(f"{project_name}/api")
        DirectoryHandler().create_dir(f"{project_name}/test_data")

        sys.stdout.write("\nDirectory structure was created.\n")