import tomllib
from pathlib import Path

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


def is_coordinate(query: str) -> bool:
        return True
    #     try:
    #         parts = [p.strip() for p in query.split(",")]
    #         if len(parts) != 2:
    #             return False
    #         lat, lon = map(float, parts)
    #         return -90 <= lat <= 90 and -180 <= lon <= 180
    #     except ValueError:
    #         return False
        
from geopy.geocoders import Nominatim
from src.utils import helpers

def get_location_coordinates(location_name: str) -> tuple[int]:
    geolocator = Nominatim(user_agent=helpers.generate_useragent())
    coordinates = geolocator.geocode(location_name)
    
    return (coordinates.latitude, coordinates.longitude)