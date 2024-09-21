from loguru import logger

from eurydice_test_framework.core.wrappers.docker import DockerWr
from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.core.management.directory_handler import \
    DirectoryHandler
from eurydice_test_framework.src.config import get_yaml_config
from eurydice_test_framework.src.database.handler import DatabaseHandler
from eurydice_test_framework.templates import CONFIG_YAML, DATASOURCE_YAML, DASHBOARD_YAML, DASHBOARD_JSON


class ProjectCommandGroup(BaseGroup):
    """Class for execute commands"""
    requires = {
        "init": ["project-name", "login", "password"]
    }

    def init_action(self, project_name: str, login: str, password: str):
        """Handler Init command: create directory structures

                Directory structure example:
                | tests
                |  | service_1
                |  | service_2
                | api
                |  | service_1
                |  | service_2
                | test_data
                """

        DirectoryHandler.write_to_file(
            file_name="config.yaml",
            content=CONFIG_YAML.replace("{login}", login).replace("{password}", password)
            .replace("{project}", project_name)
        )

        DirectoryHandler.write_to_file(
            file_name="datasource.yaml",
            content=DATASOURCE_YAML.replace("{login}", login).replace("{password}", password).replace("{project}",
                                                                                                      project_name)
        )

        DirectoryHandler.write_to_file(
            file_name="dashboard.yaml",
            content=DASHBOARD_YAML.replace("{project}", project_name)
        )

        DirectoryHandler.write_to_file(
            file_name="dashboard.json",
            content=DASHBOARD_JSON.replace("{project}", project_name)
        )

        config = get_yaml_config()
        network_name = f"{project_name}_network"
        db_cn_name = f"{project_name}_database"
        grafana_name = f"{project_name}_grafana"

        docker_client = DockerWr()

        if docker_client.check_is_network_exists(network_name=network_name):
            logger.debug(f"Network {network_name} already exists.")
        else:
            docker_client.networks.create(name=network_name)

        if docker_client.find_container(name=db_cn_name) is not None:
            logger.debug(f"Container {db_cn_name} already exists. It will be remove and create again.")

            docker_client.find_container(name=db_cn_name).stop()
            docker_client.find_container(name=db_cn_name).remove()

        if docker_client.find_container(name=grafana_name) is not None:
            logger.debug(f"Container {grafana_name} already exists. It will be remove and create again.")

            docker_client.find_container(name=grafana_name).stop()
            docker_client.find_container(name=grafana_name).remove()

        database = docker_client.containers.run(
            name=db_cn_name,
            hostname="postgres",
            image="postgres:latest",
            detach=True,
            ports={
                "5432/tcp": "5432"
            },
            environment={
                "POSTGRES_USER": config["database"]["login"],
                "POSTGRES_PASSWORD": config["database"]["password"],
                "POSTGRES_DB": f"{project_name}_database"
            },
            volumes={
                "/home/": {
                    "bind": "/mnt/vol_pgsql",
                    "mode": "rw"
                }
            },
            network=network_name
        )

        logger.debug("Database container was created.")

        grafana = docker_client.containers.run(
            name=grafana_name,
            image="grafana/grafana-enterprise",
            detach=True,
            ports={
                "3000/tcp": "3000"
            },
            volumes={
                "/home/": {
                    "bind": "/mnt/vol_graf",
                    "mode": "rw"
                }
            },
            network=network_name
        )

        logger.debug("Grafana container was created.")

        docker_client.wait_container_runned(
            container_name=database.name,
            retry_interval=10
        )

        docker_client.wait_container_runned(
            container_name=grafana.name,
            retry_interval=10,
        )

        grafana.put_archive(
            path="/etc/grafana/provisioning/datasources",
            data=DirectoryHandler.get_tar(path="datasource.yaml")
        )

        grafana.put_archive(
            path="/etc/grafana/provisioning/dashboards",
            data=DirectoryHandler.get_tar(path="dashboard.yaml")
        )

        grafana.exec_run(cmd="mkdir /var/lib/grafana/dashboards")

        grafana.put_archive(
            path="/var/lib/grafana/dashboards",
            data=DirectoryHandler.get_tar(path="dashboard.json")
        )

        grafana.restart()

        docker_client.wait_container_runned(
            container_name=grafana.name,
            retry_interval=10,
        )

        with DatabaseHandler(
                user=config["database"]["login"],
                password=config["database"]["password"],
                database=f"{project_name}_database"
        ) as db:
            db.create_meta_tables()

        database.stop()

        logger.debug("Database container was stopped.")

        grafana.stop()

        logger.debug("Grafana container was stopped.")

        DirectoryHandler().create_dir(project_name)
        DirectoryHandler().create_dir(f"{project_name}/tests")
        DirectoryHandler().create_dir(f"{project_name}/api")
        DirectoryHandler().create_dir(f"{project_name}/test_data")

        logger.debug("Directory structure was created.")

        logger.success("Project successfully was builded.")
