from time import sleep

from docker import from_env
from docker.models.containers import Container
from loguru import logger


class DockerWr:
    """Class wrapper for call docker functions"""

    def __init__(self):
        self.client = from_env()

    def __getattr__(self, item):
        return getattr(self.client, item)

    def find_container(self, name: str) -> Container | None:
        """Function for find docker container by name"""
        cn = [cn for cn in self.client.containers.list(all=True) if cn.name == name]

        return None if len(cn) == 0 else cn[0]

    def wait_container_runned(self, container_name: str, retry_interval: int = 2, retries: int = 5):
        """Method for wait run container"""
        retries = retries

        container = self.find_container(name=container_name)

        while True:
            sleep(retry_interval)

            if container.status == "running":
                logger.debug(f"Container {container.name} was runned.")

                break
            else:
                retries -= 1

                if retries == 0:
                    raise Exception(f"Timeout error. Container {container.name} wasn't runned.")

    def check_is_network_exists(self, network_name: str) -> bool:
        return network_name in [nw.name for nw in self.client.networks.list()]
