from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static, Label,
    Input, Button, Checkbox, Switch,
    DataTable,
    Select    
)
from textual.containers import (
    Container,
    Vertical,
    Horizontal
)
from textual import on

from typing import Any


from src import api
from src.api import endpoints
from src.utils import helpers


class WeatherCLI(App):
    BINDINGS = [("escape", "quit", "Quit app")]
    CSS_PATH = f"./style.tcss"
    
    def on_mount(self) -> None:
        self.push_screen(Dashboard("Dashboard"))

class Dashboard(Screen):
    def compose(self) -> ComposeResult:
        with Container():
            ### Sections
            with Horizontal(id="panels_container"):
                ## Favourites Section
                with Vertical(
                        id="favourites_panel",
                        classes="container--border"
                    ):

                    yield Label("favourites")
                 
                ## Query Section
                with Vertical(
                        id="query_section",
                        classes="container--border main-section"
                    ):
                    
                    with Horizontal(
                            id="query_bar"
                        ):
                        yield Input(id="query_input", placeholder="Input location name or coordinates")
                        yield Button(id="query_button", label="Query")
                        
                    with Container(
                            id="query_results",
                            classes="container--border"
                        ):

                        yield Static("", id="queried_location")

                        self.forecast_table = DataTable()
                        self.forecast_table.add_columns("date", "time", "weather", "temp", "rain (mm)", "wind spd", "wind °", "humidity (hPa)")
                        yield self.forecast_table
                        
                # Configs section
                with Vertical(id="configs_panel", classes="container--border"):
                    configs = helpers.Configs.get_all(); del configs["API"]

                    def _select_optionify_general_config_list(field: str) -> list[tuple[str, str]]:
                        config_value : list[str] = configs["general"][field]
                        options : list[tuple[str, str]] = []
                        
                        for o in config_value:
                            option_name = o[0].capitalize() + o.removeprefix(o[0])
                            option = (option_name, o)
                            
                            options.append(option)
                            
                        return options
                            

                    yield Static("Configs", id="configs_label")
                    with Vertical(id="configs_section_container"):
                        with Vertical(classes="configs_section"):
                            yield Label("Temperature unit")
                            yield Select(
                                options= _select_optionify_general_config_list("temperature_units"),
                                value=configs["settings"]["temperature_unit"]["value"],
                                allow_blank=False,
                                classes="config_value",
                                id="config_temperature_unit"
                            )
                    yield Button("Save", name="save_settings")
                        
    
    @on(Button.Pressed)
    def handle_button_press(self, event: Button.Pressed):
        if event.button.id == "query_button":
            self.handle_forecast_query()
            
        if event.button.name == "save_settings":
            new_settings : list[tuple[str, Any]] = []
            for setting in self.query(".config_value"):
                new_settings.append((setting.id.removeprefix("config_"), setting.value))
            
            helpers.Configs.update(new_settings=new_settings)
                
  
    def handle_forecast_query(self):
        query_input_value = self.query_one("#query_input", Input).value

        if helpers.Coordinate.is_coordinate(query_input_value):
            parts = [p.strip() for p in query_input_value.split(",")]
            weather_data = endpoints.get_weather(parts[0], parts[1])
        else:
            parts = helpers.Coordinate.get_location_coordinates(query_input_value)
            weather_data = endpoints.get_weather(parts[0], parts[1])
            
        self.forecast_table.clear()
        
        modeled_wdata = api.parse_forecast(weather_data)
        for timeserie in modeled_wdata.timeseries:
            serie_details = timeserie.details
            self.forecast_table.add_row(
                timeserie.date, # Date
                timeserie.time, # Time
                serie_details.weather, # Weather type (weather)
                serie_details.air_temperature, # Temperature (temp)
                serie_details.precipitation_amount, # Precipitation (rain (mm))
                serie_details.wind_speed, # Wind speed (wind spd)
                serie_details.wind_direction, # Wind direction (wind °)
                serie_details.relative_humidity # Humidity (humidity (hPa))
            )
        
        
    