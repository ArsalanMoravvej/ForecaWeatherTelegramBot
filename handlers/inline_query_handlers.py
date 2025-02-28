from telegram import Update
from telegram.ext import ContextTypes
from utils import inline_query_responses
from forecalib import foreca

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries"""
    query = update.inline_query.query
    results = []

    if query == "":
        # Default results when no query is provided
        results.append(inline_query_responses.empty_query_response)
    
    elif query.lower() == "help":
        # Help message
        results.append(inline_query_responses.help_query_response)
    
    else:
        try:
            locations = foreca.find_location(query)
        except:
            results.append(inline_query_responses.notfound_query_response)
        else:
            for loc in locations:
                # Store location object in bot_data with a unique key
                storage_key = f"location_{loc.id}"
                context.bot_data[storage_key] = loc

                loc_result = inline_query_responses.location_response(loc)
                results.append(loc_result)


    # Answer inline query
    await update.inline_query.answer(results)