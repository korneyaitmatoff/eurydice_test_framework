import yaml


def get_yaml_config():
    """Function for get config.yaml"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)
