import sys

from test_framework.core.management.commands import BaseCommand
from test_framework.core.management.directory_handler import DirectoryHandler


class AddserviceCommand(BaseCommand):
    """Add Service command class"""
    help = (
        "Command add service api, tests and test_data thet you will test"
    )
    command = "add_service"
    requires = ["project_name", "service_name"]

    def handle(self, project_name: str, service_name: str):
        for folder in ["api", "test_data", "tests"]:
            DirectoryHandler().create_dir(path=f"{project_name}/{folder}/{service_name}")

        sys.stdout.write(f"\nService {service_name} was added.\n")
