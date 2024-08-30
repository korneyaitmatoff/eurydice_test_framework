from .base_command import BaseCommand


class InitCommand(BaseCommand):
    """Init command: build directory structure"""
    help = (
        "It's command init project and creates directory structure"
    )
    command = "init"
    requires = ["project_name"]

    def handle(self, project_name: str):
        """Handler Init command: create directory structure"""
        print(project_name)
        print("init")
