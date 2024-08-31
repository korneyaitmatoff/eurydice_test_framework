import sys

from eurydice_test_framework.core.management.commands import BaseCommand
from eurydice_test_framework.core.management.directory_handler import DirectoryHandler
from eurydice_test_framework.templates import test_template, api_template


class AddserviceCommand(BaseCommand):
    """Add Service command class"""
    help = (
        "Command add service api, tests and test_data thet you will test"
    )
    command = "add_service"
    requires = ["project_name", "service_name"]

    def handle(self, project_name: str, service_name: str):
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
