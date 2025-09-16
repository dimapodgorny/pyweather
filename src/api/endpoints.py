from src.api.client import request_forecast_from_coordinates


def get_weather(lat: float, lon: float):
    try:
        data = request_forecast_from_coordinates(lat=lat, lon=lon)
        return data
    except Exception as exception:
        return f"Failed to get weather: {exception}"