from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.core.management.tests_handler import run_tests
from eurydice_test_framework.src.database.handler import DatabaseHandler
from eurydice_test_framework.core.database.tables import TestsRun
from eurydice_test_framework.src.config import get_yaml_config
from eurydice_test_framework.core.wrappers.docker import DockerWr


class TestsCommandGroup(BaseGroup):
    requires = {
        "run": ["mark"]
    }

    def run_action(self, mark: str):
        result = run_tests(mark=mark)
        config = get_yaml_config()
        container = (dwr := DockerWr()).find_container(name=f"{config['project']['name']}_database")

        container.start()
        dwr.wait_container_runned(container_name=container.name)

        with DatabaseHandler(
                user=config["database"]["login"],
                password=config["database"]["password"],
                database=f"{config['project']['name']}_database"
        ) as db:
            for item in result:
                db.insert(
                    table=TestsRun,
                    data=item
                )

        container.stop()
