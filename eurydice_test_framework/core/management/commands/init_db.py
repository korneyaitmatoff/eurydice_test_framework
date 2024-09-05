from eurydice_test_framework.core.management.commands import BaseCommand
from eurydice_test_framework.templates import DC_YAML, ENV


class InitdbCommand(BaseCommand):
    help = (
        "Command for build local database"
    )
    command = "init_db"
    requires = ["user", "password", "database"]

    def handle(self, user: str, password: str, database: str):
        (f := open("docker-compose.yaml", "w")) \
            .write(DC_YAML)
        f.close()

        (f := open(".env", "w")). \
            write(ENV
                  .replace("{POSTGRES_USER}", user)
                  .replace("{POSTGRES_PASSWORD}", password)
                  .replace("{POSTGRES_DB}", database)
                  )
        f.close()
