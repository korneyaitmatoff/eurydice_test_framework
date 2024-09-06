import sys
from os import mkdir, rmdir


class DirectoryHandler:
    def create_dir(self, path: str):
        try:
            mkdir(path)
        except FileExistsError:
            sys.stdout.write(f"{path} already exists\n")
        except FileNotFoundError:
            sys.stdout.write(f"{path} is wrong\nTry again\n")
