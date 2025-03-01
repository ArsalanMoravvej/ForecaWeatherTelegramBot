

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from forecalib import foreca, models


def daily_weather_response(location: models.Location):
    # Get daily forecast using the location object
    forecast = foreca.fetch_daily_weather(location)
    # Format the forecast data
    message = f"Daily Forecast for <b>{location.name}</b>\n"
    for day in forecast:
        message += "\n----"
        message += f"\n<b>{day.date.strftime("%A")}:</b> {day.date}\n"
        message += f"\n<b>Max Temperature:</b> {day.max_temperature_celsius}\n"
        message += f"<b>Min Temperature:</b> {day.min_temperature_celsius}\n"
        message += f"<b>Precipitation:</b> {day.rainfall_mm}mm  ({day.rain_probability_percent}%)\n"
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
    message  = f"<b>📍 - {location.name} Hourly Forecast</b>\n"
    message += f"<b>📅 - {forecast[0].timestamp.date().strftime("%A")}</b> - "
    message += f"{forecast[0].timestamp.date().strftime("%B")}"
    message += f" {forecast[0].timestamp.day}\n"
    for hour in forecast:
        message += f"_________________\n"
        message += f"\n<b>⏰ Time:</b> {hour.time_24_hour}:00\n\n"
        message += f"<b>⛅️ Weather:</b> {hour.weather_description}\n"
        message += f"<b>🌡 Temperature:</b> {hour.temperature_celsius} °C\n"
        message += f"<b>👤 Feels Like:</b> {hour.feels_like_celsius} °C\n"
        message += f"<b>💧 Rel. Humidity:</b> {hour.relative_humidity_percent} %\n"
        message += f"<b>🌬 Wind:</b> {hour.wind_speed_kmh} KM/H\n"
        message += f"<b>🕶 UV Index:</b> {hour.uv_index}\n"
        message += f"<b>🍃 Air Quality:</b> {hour.air_quality_index}\n"
                
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