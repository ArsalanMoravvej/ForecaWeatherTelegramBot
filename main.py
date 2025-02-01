from telegram.ext import (
    Application,
    InlineQueryHandler,
    CallbackQueryHandler,
    CommandHandler,
)

from handlers.inline_query_handlers import handle_inline_query
from handlers.button_callback_handlers import button_callback
from handlers.command_handlers import start_command

from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(InlineQueryHandler(handle_inline_query))
    application.add_handler(CallbackQueryHandler(button_callback))  


    # Start polling
    print("Bot started...")
    application.run_polling(poll_interval=1)

if __name__ == '__main__':
    main()