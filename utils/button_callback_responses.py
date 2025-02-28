

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
    message = f"Hourly Forecast for {location.name} - {forecast[0].timestamp}:\n"
    for hour in forecast:
        message += "----"
        message += f"\n<b>Time:</b> {hour.time_24_hour}\n"
        message += f"\n<b>Temperature:</b> {hour.temperature_celsius}\n"
        message += f"<b>Feels Like:</b> {hour.feels_like_celsius}\n"
                
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