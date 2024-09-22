import io
import tarfile
from os import mkdir

from loguru import logger


class DirectoryHandler:
    """Class for directory methods"""
    def create_dir(self, path: str):
        """Method for create directory"""
        try:
            mkdir(path)
        except FileExistsError:
            logger.error(f"{path} already exists\n")
        except FileNotFoundError:
            logger.error(f"{path} is wrong\nTry again\n")

    @staticmethod
    def get_tar(path: str):
        """Method for archive file to tar"""
        tar = io.BytesIO()

        with tarfile.open(fileobj=tar, mode="w") as t:
            t.add(path)
        tar.seek(0)

        return tar

    @staticmethod
    def write_to_file(file_name: str, content: str):
        with open(file_name, "w") as f:
            f.write(content)

        logger.debug(f"File {file_name} was created.")
