from telegram import (
    Update,
)
from telegram.ext import ContextTypes
from forecalib import models
from utils import button_callback_responses


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

            message, reply_markup = button_callback_responses.daily_weather_response(location)


        elif action == "hourly":

            message, reply_markup = button_callback_responses.hourly_weather_response(location)

        await query.edit_message_text(
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    except Exception as e:
        await query.edit_message_text(
            text=f"Sorry, couldn't fetch the forecast. Error: {str(e)}"
        )        
