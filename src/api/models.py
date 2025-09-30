from dataclasses import dataclass
from src.utils.helpers import Configs

@dataclass
class WeatherDetails:
    air_temperature: float
    weather: str
    precipitation_amount: float
    wind_speed: float
    wind_direction: float
    relative_humidity: float
    

@dataclass
class ForecastTimeStep:
    date: str
    time: str
    details: WeatherDetails

@dataclass
class Forecast:
    timeseries: list[ForecastTimeStep]

def parse_forecast(json_data) -> Forecast:
    timeseries = []
    
    for entry in json_data["properties"]["timeseries"]:
        
        details_instant = entry["data"]["instant"]["details"]
        details_next_1_hours = None
        try:
            details_next_1_hours = entry["data"]["next_1_hours"]
        except:
            continue
        _time : str = entry["time"]
        _time_parts = [p.strip() for p in _time.split("T")]
        
        temperature_unit = Configs.get_specific("temperature_unit")
        
        match temperature_unit:
            case "celsius":
                timeseries.append(
                    ForecastTimeStep(
                        date=_time_parts[0],
                        time=_time_parts[1].removesuffix("Z"),
                        details=WeatherDetails(
                            air_temperature=details_instant.get("air_temperature"),
                            weather=details_next_1_hours["summary"]["symbol_code"],
                            wind_speed=details_instant.get("wind_speed"),
                            precipitation_amount=details_next_1_hours["details"]["precipitation_amount"],
                            wind_direction=details_instant.get("wind_from_direction"),
                            relative_humidity=details_instant.get("relative_humidity")
                        )
                    )
                )
            case "fahrenheit":
                displayed_air_temp = (details_instant.get("air_temperature") * 9/5) + 32
                timeseries.append(
                    ForecastTimeStep(
                        date=_time_parts[0],
                        time=_time_parts[1].removesuffix("Z"),
                        details=WeatherDetails(
                            weather = details_next_1_hours["summary"]["symbol_code"],
                            air_temperature = displayed_air_temp,
                            precipitation_amount = details_next_1_hours["details"]["precipitation_amount"],
                            wind_speed = details_instant.get("wind_speed"),
                            wind_direction = details_instant.get("wind_from_direction"),
                            relative_humidity = details_instant.get("relative_humidity")
                        )
                    )
                )
            case "kelvin":
                displayed_air_temp = (details_instant.get("air_temperature") + 273.15) 
                timeseries.append(
                    ForecastTimeStep(
                        date=_time_parts[0],
                        time=_time_parts[1].removesuffix("Z"),
                        details=WeatherDetails(
                            weather = details_next_1_hours["summary"]["symbol_code"],
                            air_temperature = displayed_air_temp,
                            precipitation_amount = details_next_1_hours["details"]["precipitation_amount"],
                            wind_speed = details_instant.get("wind_speed"),
                            wind_direction = details_instant.get("wind_from_direction"),
                            relative_humidity = details_instant.get("relative_humidity")
                        )
                    )
                )
    return Forecast(timeseries=timeseries)