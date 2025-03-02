from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime, time, date as dateclass

weather_code_emojis = {
    # Daytime Weather Codes
    "d000": "☀️",
    "d100": "🌤️",
    "d200": "⛅",
    "d210": "⛅🌧️",
    "d211": "⛅🌨️",
    "d212": "⛅❄️",
    "d220": "⛅🌦️",
    "d221": "⛅🌨️",
    "d222": "⛅❄️",
    "d240": "⛅⚡🌧️",
    "d300": "🌥️",
    "d310": "🌥️🌧️",
    "d311": "🌥️🌨️",
    "d312": "🌥️❄️",
    "d320": "🌥️🌦️",
    "d321": "🌥️🌨️",
    "d322": "🌥️❄️",
    "d340": "🌥️⚡🌧️",
    "d400": "☁️",
    "d410": "☁️🌧️",
    "d411": "☁️🌨️",
    "d412": "☁️❄️",
    "d420": "☁️🌦️",
    "d421": "☁️🌨️",
    "d422": "☁️❄️",
    "d430": "☁️🌧️",
    "d431": "☁️🌨️",
    "d432": "☁️❄️",
    "d440": "☁️⚡🌧️",
    "d500": "🌤️",
    "d600": "🌫️",

    # Nighttime Weather Codes
    "n000": "🌙",
    "n100": "🌙☁️",
    "n200": "🌙☁️",
    "n210": "🌙☁️🌧️",
    "n211": "🌙☁️🌨️",
    "n212": "🌙☁️❄️",
    "n220": "🌙☁️🌦️",
    "n221": "🌙☁️🌨️",
    "n222": "🌙☁️❄️",
    "n240": "🌙☁️⚡🌧️",
    "n300": "🌙☁️",
    "n310": "🌙☁️🌧️",
    "n311": "🌙☁️🌨️",
    "n312": "🌙☁️❄️",
    "n320": "🌙☁️🌦️",
    "n321": "🌙☁️🌨️",
    "n322": "🌙☁️❄️",
    "n340": "🌙☁️⚡🌧️",
    "n400": "🌙☁️",
    "n410": "🌙☁️🌧️",
    "n411": "🌙☁️🌨️",
    "n412": "🌙☁️❄️",
    "n420": "🌙☁️🌦️",
    "n421": "🌙☁️🌨️",
    "n422": "🌙☁️❄️",
    "n430": "🌙☁️🌧️",
    "n431": "🌙☁️🌨️",
    "n432": "🌙☁️❄️",
    "n440": "🌙☁️⚡🌧️",
    "n500": "🌙☁️",
    "n600": "🌙🌫️"
}

def get_weather_emoji(code):
    return weather_code_emojis.get(code, "❓")  # Default to unknown emoji


class WindDirections:
    directions = {
        "N": "⬇️",
        "NE": "↙️",
        "E": "⬅️",
        "SE": "↖️",
        "S": "⬆️",
        "SW": "↗️",
        "W": "➡️",
        "NW": "↘️"
    }

    @classmethod
    def get_direction(cls, key: str) -> str:
        return cls.directions.get(key, "Unknown direction")


class MoonPhases:
    phases = {
        "newMoon": "🌑",
        "waxingCrescentMoon": "🌒",
        "firstQuarterMoon": "🌓",
        "waxingGibbousMoon": "🌔",
        "fullMoon": "🌕",
        "waningGibbousMoon": "🌖",
        "lastQuarterMoon": "🌗",
        "waningCrescentMoon": "🌘"
    }

    @classmethod
    def get_phase(cls, key: str) -> str:
        return cls.phases.get(key, "Unknown phase")


class HourEmojis:
    emojis = {
        "12 AM": "🕛",
        "1 AM": "🕐",
        "2 AM": "🕑",
        "3 AM": "🕒",
        "4 AM": "🕓",
        "5 AM": "🕔",
        "6 AM": "🕕",
        "7 AM": "🕖",
        "8 AM": "🕗",
        "9 AM": "🕘",
        "10 AM": "🕙",
        "11 AM": "🕚",
        "12 PM": "🕛",
        "1 PM": "🕐",
        "2 PM": "🕑",
        "3 PM": "🕒",
        "4 PM": "🕓",
        "5 PM": "🕔",
        "6 PM": "🕕",
        "7 PM": "🕖",
        "8 PM": "🕗",
        "9 PM": "🕘",
        "10 PM": "🕙",
        "11 PM": "🕚"
    }

    @classmethod
    def get_emoji(cls, key: str) -> str:
        return cls.emojis.get(key, "Unknown time")


class Location(BaseModel):
    id: str
    name: str
    countryName: str
    countryId: str
    timezone: str
    population: Optional[int]
    lon: float
    lat: float

    @field_validator("lon", "lat", mode="before")
    def convert_to_string(cls, value):
        return str(value)


class DailyWeather(BaseModel):

    location_info: Location

    # 1. Date and Forecast Metadata
    date: dateclass = Field(alias="date")
    last_updated: datetime = Field(alias="updated")
    
    # 2. Weather Conditions
    weather_symbol: str = Field(alias="symb")
    min_temperature_celsius: float = Field(alias="tmin")
    max_temperature_celsius: float = Field(alias="tmax")
    relative_humidity_percent: float = Field(alias="rhum")
    uv_index: float = Field(alias="uvi")

    # 3. Rain and Snow Data
    rainfall_mm: float = Field(alias="rain")
    rain_probability_percent: float = Field(alias="rainp")
    snow_probability_percent: float = Field(alias="snowp")
    snowfall_mm: float = Field(alias="snowff")
    
    # 4. Wind Details
    wind_direction_degrees: float = Field(alias="windd")
    wind_speed_kmh: float = Field(alias="winds")
    
    # 5. Sun and Moon Details
    sunrise_time: time = Field(alias="sunrise")
    sunset_time: time = Field(alias="sunset")
    day_length_seconds: int = Field(alias="daylen")
    
    moonrise_time: Optional[time] = Field(alias="moonrise")
    moonset_time: Optional[time] = Field(alias="moonset")
    is_moon_up: bool = Field(alias="moonup")
    moon_phase: str = Field(alias="moonphase")
    moon_phase_title: str = Field(alias="moonphaseTitle")
    
    @field_validator("moonrise_time", "moonset_time", mode="before")
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            time: lambda v: v.strftime('%H:%M:%S'),
        }


class HourlyWeather(BaseModel):

    location_info: Location

    # 1. Timestamps and Forecast Times
    timestamp: datetime = Field(alias="time")
    last_updated: datetime = Field(alias="updated")
    forecast_datetime: datetime = Field(alias="dateObject")
    time_12_hour: str = Field(alias="h12")
    time_24_hour: str = Field(alias="h24")
    
    # 2. Weather Conditions
    weather_symbol: str = Field(alias="symb")
    weather_description: str = Field(alias="wx")
    weather_class: str = Field(alias="weatherClass")
    air_quality_index: int = Field(alias="aqi")
    uv_index: int = Field(alias="uvi")
    
    # 3. Temperature Details
    temperature_celsius: int = Field(alias="temp")
    feels_like_celsius: int = Field(alias="flike")
    dew_point_celsius: int = Field(alias="dewp")

    temperature_fahrenheit: float = Field(alias="tempf")
    feels_like_fahrenheit: float = Field(alias="flikef")
    dew_point_fahrenheit: float = Field(alias="dewpf")
    
    # 4. Wind Details
    wind_direction_degrees: float = Field(alias="windd")
    wind_direction_cardinal: str = Field(alias="windCardinal")

    wind_speed_kmh: int = Field(alias="windskmh")
    wind_speed_mph: int = Field(alias="windsmph")
    wind_speed_beaufort: float = Field(alias="windsbft")

    max_wind_speed_kmh: int = Field(alias="maxwindkmh")
    max_wind_speed_mph: int = Field(alias="maxwindmph")
    max_wind_beaufort: float = Field(alias="maxwindbft")
    
    # 5. Rainfall and Snowfall
    rainfall_mm: float = Field(alias="rain")
    rainfall_mm_long: float = Field(alias="rainl")
    snowfall_mm: float = Field(alias="snowff")

    rainfall_inches: float = Field(alias="rainin")
    rainfall_long_inches: float = Field(alias="rainlin")
    snowfall_inches: float = Field(alias="snowffin")

    rain_probability_percent: int = Field(alias="rainp")
    snow_probability_percent: int = Field(alias="snowp")

    
    # 6. Atmospheric and Visibility Data
    relative_humidity_percent: int = Field(alias="rhum")
    pressure_hpa: float = Field(alias="pres")
    pressure_inhg: float = Field(alias="presinhg")
    pressure_mmhg: float = Field(alias="presmmhg")
    visibility_miles: Optional[float] = Field(alias="vismi")
    
    # 7. Additional Information
    day_steps: Optional[float] = Field(alias="daysteps")
    
    class Config:
        populate_by_name = True
