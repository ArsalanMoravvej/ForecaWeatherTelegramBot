from telegram import InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, Update
from forecalib import models

empty_query_response = InlineQueryResultArticle(
    id="default",
    title="How to use this bot",
    description="Click here to learn how to use this bot",
    input_message_content=InputTextMessageContent(
        "Type the city of Your choice after @Mangolinebot to search for it!"
    )
)

help_query_response = InlineQueryResultArticle(
    id="help",
    title="Help",
    description="Show help message",
    input_message_content=InputTextMessageContent(
            "Available commands:\n"
            "- Type the city of Your choice after @Mangolinebot to search for it\n"
            "- Type 'help' to see this message"
        )
    )
notfound_query_response = InlineQueryResultArticle(
    id="notFound",
    title="Coudn't find what you're searching for.",
    description="Click here to learn how to use this bot",
    input_message_content=InputTextMessageContent(
    "Type the city of Your choice after @Mangolinebot to search for it!"
    )
)

def location_response(loc: models.Location) -> InlineKeyboardMarkup:

# Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("Daily Forecast", callback_data=f"daily_{loc.id}"),
            InlineKeyboardButton("Hourly Forecast", callback_data=f"hourly_{loc.id}")
        ],
        # Second row - single button with URL
        [
            InlineKeyboardButton("Open In Foreca  🌐", url=f"https://www.foreca.com/{loc.id}/{loc.name}-{loc.countryName}")
        ],
        [
            InlineKeyboardButton("Another Location 📍", switch_inline_query_current_chat="")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

# Default results when no query is provided

    location_result = InlineQueryResultArticle(
    id=loc.id,
    title=loc.name,
    description=f"{loc.name}-{loc.countryName}",
    input_message_content=InputTextMessageContent(
        f"<b>Your Location of choice:</b> {loc.name}\n"
        f"<b>country:</b> {loc.countryName}\n"
        f"<b>timezone:</b> {loc.timezone}\n"
        f"<b>population:</b> {loc.population}\n"
        f"<b>lon:</b> {loc.lon}\n"
        f"<b>lat:</b> {loc.lat}\n",
        parse_mode='HTML'
        ),
    reply_markup=reply_markup
    )

    return location_result