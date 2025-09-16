# Textual imports
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, Button, DataTable
from textual import on

# Project imports

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
            with Horizontal(id="sections_container"):
                ## Favourites Section
                with Vertical(
                    id="favourite_section",
                    classes="container--border"
                    ):
                    yield Static("favourites")
                
                ## Query Section
                with Vertical(
                    id="query_section",
                    classes="container--border main-section"
                    ):
                    with Horizontal(
                        id="query_bar"
                        ):

                        yield Input(
                            id="query_input",
                            placeholder="Input location name or coordinates"
                            )

                        yield Button(
                            id="query_button",
                            label="Query"
                            )
                        
                    with Container(
                        id="query_results",
                        classes="container--border"
                        ):

                        yield Static("", id="queried_location")

                        self.forecast_table = DataTable()
                        self.forecast_table.add_columns("date", "time", "weather", "temp", "rain (mm)", "wind spd", "wind °", "humidity (hPa)")
                        yield self.forecast_table
                        
                # something section
                with Vertical(id="some_section", classes="container--border"):
                    yield Static("right panel (settings probably)")
        
    @on(Button.Pressed)
    def handle_button_press(self, event: Button.Pressed):
        if event.button.id == "query_button":
            self.handle_forecast_query()
            
    def handle_forecast_query(self):
        query_input_value = self.query_one("#query_input", Input).value
        if helpers.is_coordinate(query_input_value):
            parts = [p.strip() for p in query_input_value.split(",")]
            weather_data = endpoints.get_weather(parts[0], parts[1])
        
        modeled_wdata = api.parse_forecast(weather_data)
        for timeserie in modeled_wdata.timeseries:
            serie_details = timeserie.details
            self.forecast_table.add_row(
                timeserie.date, # Date
                timeserie.time, # Time
                serie_details.air_temperature, # Temperature (temp)
                serie_details.weather, # Weather type (weather)
                serie_details.precipitation_amount, # Precipitation (rain (mm))
                serie_details.wind_speed, # Wind speed (wind spd)
                serie_details.wind_direction, # Wind direction (wind °)
                serie_details.relative_humidity # Humidity (humidity (hPa))
            )
            
        
            
        self.query_one("#query_input", Input).clear()
        
        
    