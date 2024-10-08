import sys

from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.core.management.directory_handler import \
    DirectoryHandler
from eurydice_test_framework.src.config import get_yaml_config
from eurydice_test_framework.templates import api_template, test_template


class ServiceCommandGroup(BaseGroup):
    requires = {
        "add": ["service-name"]
    }

    def add_action(self, service_name: str):
        """Method for add service to project"""
        project_name = get_yaml_config()['project']['name']

        try:
            for folder in ["api", "test_data", "tests"]:
                DirectoryHandler().create_dir(path=f"{project_name}/{folder}/{service_name}")

                if folder == "tests":
                    (f := open(f"{project_name}/{folder}/{service_name}/test_{service_name}.py", "a")) \
                        .write(test_template.replace("{test_name}", service_name.capitalize()))
                    f.close()
                if folder == "api":
                    (f := open(f"{project_name}/{folder}/{service_name}/{service_name}.py", "a")) \
                        .write(api_template.replace("{api_name}", service_name.capitalize()))
                    f.close()

            sys.stdout.write(f"\nService {service_name} was added.\n")
        except FileNotFoundError:
            sys.stdout.write(f"Maybe incorrect project name {project_name}?")
