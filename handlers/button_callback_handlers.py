from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
)
from telegram.ext import ContextTypes
from forecalib import foreca, models


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    # Parse the callback data
    action, location_id = query.data.split('_')
    
    # Retrieve the location object from bot_data
    storage_key = f"location_{location_id}"
    location: models.Location = context.bot_data.get(storage_key)

    if location is None:
        await query.edit_message_text("Sorry, location data expired. Please search again.")
        return


    try:
        if action == "daily":
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


        elif action == "hourly":

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

        await query.edit_message_text(
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    except Exception as e:
        await query.edit_message_text(
            text=f"Sorry, couldn't fetch the forecast. Error: {str(e)}"
        )        
