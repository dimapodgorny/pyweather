import json
from src.utils import helpers

def get_config(config_name: str):
    return helpers.Configs.get_all()["API"][config_name]