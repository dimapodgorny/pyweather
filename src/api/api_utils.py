import json

def get_config(config_name: str):
    with open(f"./src/config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        
    return data["API"][config_name]