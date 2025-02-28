from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    help_text = """
Hello I'm a test bot for telling you the weather in your city!
"""
    await update.message.reply_text(help_text)
