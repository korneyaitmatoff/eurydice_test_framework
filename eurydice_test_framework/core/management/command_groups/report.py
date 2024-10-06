from loguru import logger

from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.src.config import get_yaml_config
from eurydice_test_framework.core.wrappers.docker import DockerWr


class ReportCommandGroup(BaseGroup):
    """Class for report management"""
    requires = {
        "run": []
    }

    def run_action(self):
        """Method for run grafana"""
        config = get_yaml_config()
        db_container = (dwr := DockerWr()).find_container(name=f"{config['project']['name']}_database")
        grafana_container = dwr.find_container(name=f"{config['project']['name']}_grafana")

        db_container.start()
        dwr.wait_container_runned(container_name=db_container.name)

        grafana_container.start()
        dwr.wait_container_runned(container_name=grafana_container.name)

        logger.success(f"Report's dashboard was runned on: http://localhost:3000")
