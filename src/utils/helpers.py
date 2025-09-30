import tomllib
import json
from typing import Any
from pathlib import Path
from geopy.geocoders import Nominatim
import re

# def get_project_metadata(*fields: str):
def get_project_metadata():
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    with pyproject_path.open("rb") as metadata_raw:
        data = tomllib.load(metadata_raw)
        
    project : dict = data.get("project", {})
    name = project.get("name", "unknown")
    version = project.get("version", "unknown")
    homepage = project.get("urls", {}).get("homepage", "")
    
    return name, version, homepage

def generate_useragent() -> str:
    name, version, homepage = get_project_metadata()
    return f"{name}/{version} ({homepage})"

class Configs:
    global CONFIG_PATH
    CONFIG_PATH = f"./src/config.json"
    @staticmethod
    def get_all() -> dict:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            data : dict = json.load(file)
        return data
    
    @staticmethod
    def get_specific(setting_name: str) -> Any:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            data : dict = json.load(file)
            
        return data["settings"][setting_name]["value"]
            
        
    
    @staticmethod
    def update(new_settings: list[tuple[str, Any]]) -> None:
        """a setting using a tuple. first item in tuple is the updated setting's string name, 2nd is its value"""
        with open(CONFIG_PATH, "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            for setting in new_settings:
                if setting[0] in data["settings"].keys():
                    data["settings"][setting[0]]["value"] = setting[1]
                else:
                    raise ValueError()
            
            file.seek(0)
            json.dump(data, file)
            file.truncate()
        
    @staticmethod
    def reset_all():
        resat_settings = []
        with open(CONFIG_PATH, "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            for name in data["settings"].keys():
                if data["settings"][name]["value"] == data["settings"][name]["default"]:
                    resat_settings.append(name)
                    
                data["settings"][name]["value"] = data["settings"][name]["default"]
                
            file.seek(0)
            json.dump(data, file)
            file.truncate()
        return resat_settings


class Coordinate:
    @staticmethod
    def is_coordinate(coord: str) -> bool:
        match = re.match(r"^\s*([-+]?\d+(\.\d+)?)\s*[, ]\s*([-+]?\d+(\.\d+)?)\s*$", coord)
        if not match:
            return False
        
        lat = float(match.group(1))
        lon = float(match.group(3))
        
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def get_location_coordinates(location: str) -> tuple[int]:
        geolocator = Nominatim(user_agent=generate_useragent())
        coordinates = geolocator.geocode(location)
        
        return (coordinates.latitude, coordinates.longitude)
    
    @staticmethod
    def to_queryable(system: str, original_coordinate) -> tuple[float, float]:
        """_summary_
        Converts an known Geographic Coordinate System (GCS) into the Latitude/Longitude system which can be used for MET API Locationforecast queries.
        
        Params:
            `coordinate_system: str` tells
        """
        
        if not system in Coordinate.GCS:
            raise ValueError
    