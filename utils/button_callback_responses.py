

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from forecalib import foreca, models


def daily_weather_response(location: models.Location):
    forecast = foreca.fetch_daily_weather(location)
    
    # Format the forecast data
    message = "<b>"
    message += f"📍 - {location.name} Daily Forecast\n\n"
    
    for day in forecast:
        message += "\n"
        message += f"📅 {day.date.strftime('%A')} - {day.date.strftime('%B')} {day.date.day} | {models.get_weather_emoji(day.weather_symbol)}\n"
        message += f"🌡 Max: {day.max_temperature_celsius} °C | Min: {day.min_temperature_celsius} °C\n"
        message += f"💧 Rel. Hum: {day.relative_humidity_percent} %\n"
        
        if day.rainfall_mm >= 0.1:
            message += f"🌧 Rainfall: {round(day.rainfall_mm, 1)} mm ({day.rain_probability_percent}%)\n"
        
        if day.snowfall_mm >= 0.1:
            message += f"❄️ Snowfall: {round(day.snowfall_mm, 1)} mm ({day.snow_probability_percent}%)\n"
            
        message += f"🌬 Wind: {day.wind_speed_kmh} kmh {models.WindDirections.get_direction_from_degrees(day.wind_direction_degrees)}\n"
        
        if day.uv_index > 0:
            message += f"🕶 UV Index: {day.uv_index}\n"
            
        message += f"🌞 ↑{day.sunrise_time.strftime('%H:%M')} | ↓{day.sunset_time.strftime('%H:%M')} | ⏱️ {day.day_length_minutes//60}h {day.day_length_minutes%60}m\n"
        
        if day.moonrise_time and day.moonset_time:
            message += f"🌙 ↑{day.moonrise_time.strftime('%H:%M')} | ↓{day.moonset_time.strftime('%H:%M')} | {models.MoonPhases.get_phase(day.moon_phase_title)}\n\n"

    
    message += "</b>"
                
    keyboard = [
        [
            InlineKeyboardButton("Hourly Forecast", callback_data=f"hourly_{location.id}")                    
        ],
        [
            InlineKeyboardButton("Open In Foreca 🌐", url=f"https://www.foreca.com/{location.id}/{location.name}-{location.countryName}/10-day-forecast")
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
        message += f"{models.HourEmojis.get_emoji(hour.time_12_hour)} {hour.time_12_hour} | {models.get_weather_emoji(hour.weather_symbol)}\n"
        message += f"🔹 {hour.weather_description}\n"
        message += f"🌡 Temp: {hour.temperature_celsius} °C | 👤 F.Like: {hour.feels_like_celsius} °C\n"
        message += f"💧 Rel. Hum: {hour.relative_humidity_percent} %\n"
        
        if hour.rainfall_mm >= 0.1:
            message += f"🌧 Rainfall: {round(hour.rainfall_mm,1)} mm ({hour.rain_probability_percent}%)\n"
        
        if hour.snowfall_mm >= 0.1:
            message += f"❄️ Snowfall: {round(hour.snowfall_mm,1)} mm ({hour.snow_probability_percent}%)\n"

        message += f"🌬 Wind: {hour.wind_speed_kmh} kmh {models.WindDirections.get_direction(hour.wind_direction_cardinal)}\n"
        
        message += f"🍃 Air Quality: {hour.air_quality_index}"
        if hour.uv_index > 0:
            message += f" | 🕶 UV Index: {hour.uv_index}\n"
        else:
            message += "\n"
    
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