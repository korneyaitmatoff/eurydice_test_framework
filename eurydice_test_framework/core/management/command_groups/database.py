from eurydice_test_framework.core.management.command_groups import BaseGroup
from eurydice_test_framework.templates import DC_YAML, ENV


class DatabaseCommandGroup(BaseGroup):
    requires = {
        "init": ["user", "password", "database"]
    }

    def init_action(self, user: str, password: str, database: str):
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
