

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from forecalib import foreca, models


def daily_weather_response(location: models.Location):
    # Get daily forecast using the location object
    forecast = foreca.fetch_daily_weather(location)
    # Format the forecast data
    message = f"Daily Forecast for {location.name}\n"
    for day in forecast:
        message += "\n----"
        message += f"\n{day.date.strftime("%A")}: {day.date}\n"
        message += f"\nMax Temperature: {day.max_temperature_celsius}\n"
        message += f"Min Temperature: {day.min_temperature_celsius}\n"
        message += f"Precipitation: {day.rainfall_mm}mm  ({day.rain_probability_percent}%)\n"
    keyboard = [
        [
            InlineKeyboardButton("Hourly Forecast", callback_data=f"hourly_{location.id}")                    
        ],
        [
            InlineKeyboardButton("Open In Foreca  🌐", url=f"https://www.foreca.com/{location.id}/{location.name}-{location.countryName}/10-day-forecast")
        ],
        [
            InlineKeyboardButton("Another Location 📍", switch_inline_query_current_chat="")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return message, reply_markup
 
def hourly_weather_response(location: models.Location):

    # Get hourly forecast using the location object
    forecast = foreca.fetch_hourly_weather(location)
    # Format the forecast data
    message = "<b>"
    message += f"📍 - {location.name} Hourly Forecast\n"
    message += (
        f"📅 - {forecast[0].timestamp.date().strftime("%A")} - "
        f"{forecast[0].timestamp.date().strftime("%B")} "
        f"{forecast[0].timestamp.day}\n"
        )
    for hour in forecast:
        message += f"\n"
        message += f"{models.HourEmojis.get_emoji(hour.time_12_hour)} {hour.time_12_hour}\n"
        message += f"🔹 {hour.weather_description} {models.get_weather_emoji(hour.weather_symbol)}\n"
        message += f"🌡 Temp: {hour.temperature_celsius} °C\n"
        message += f"👤 F.Like: {hour.feels_like_celsius} °C\n"
        message += f"💧 Rel. Hum: {hour.relative_humidity_percent} %\n"
        
        if hour.rainfall_mm >= 0.1:
            message += f"🌧 Rainfall: {round(hour.rainfall_mm,1)} mm\n"
        
        if hour.snowfall_mm >= 0.1:
            message += f"❄️ Snowfall: {round(hour.snowfall_mm,1)} mm\n"

        message += f"🌬 Wind: {hour.wind_speed_kmh} KM/H in {models.WindDirections.get_direction(hour.wind_direction_cardinal)}\n"

        if hour.uv_index > 0:
            message += f"🕶 UV Index: {hour.uv_index}\n"
        
        message += f"🍃 Air Quality: {hour.air_quality_index}\n"
    
    message += "</b>"
                
    keyboard = [
        [
            InlineKeyboardButton("Daily Forecast", callback_data=f"daily_{location.id}")                    
        ],
        [
            InlineKeyboardButton("Open In Foreca 🌐", url=f"https://www.foreca.com/{location.id}/{location.name}-{location.countryName}/hourly?day=0")
        ],
        [
            InlineKeyboardButton("Another Location 📍", switch_inline_query_current_chat="")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return message, reply_markup