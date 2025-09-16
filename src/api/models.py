from dataclasses import dataclass

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
        
        timeseries.append(
            ForecastTimeStep(
                date=_time_parts[0],
                time=_time_parts[1].removesuffix("Z"),
                details=WeatherDetails(
                    air_temperature=details_instant.get("air_temperature"),
                    weather=details_next_1_hours["summary"]["symbol_code"],
                    precipitation_amount=details_next_1_hours["details"]["precipitation_amount"],
                    wind_speed=details_instant.get("wind_speed"),
                    wind_direction=details_instant.get("wind_from_direction"),
                    relative_humidity=details_instant.get("relative_humidity")
                )
            )
        )
        
        
    return Forecast(timeseries=timeseries)