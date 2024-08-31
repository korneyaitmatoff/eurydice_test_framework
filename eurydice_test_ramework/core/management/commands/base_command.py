"""Class command template"""


class BaseCommand:
    help: str
    command: str
    requires: list[str] = []

    def handle(self, *args): ...
