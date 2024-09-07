from sys import stdout

from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.core.management.directory_handler import \
    DirectoryHandler


class ProjectCommandGroup(BaseGroup):
    requires = {
        "init": ["project-name"]
    }

    def init_action(self, project_name: str):
        """Handler Init command: create directory structures

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

        stdout.write("\nDirectory structure was created.\n")
