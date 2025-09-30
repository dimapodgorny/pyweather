import requests
from src.api import api_utils

from src.utils import helpers

def request_forecast_from_coordinates(lat: float, lon: float):    
    url = str(api_utils.get_config("BASE_URL"))
    headers = {
        "User-Agent": helpers.generate_useragent()
    }
    params = {
        "lat": lat,
        "lon": lon
    }
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")