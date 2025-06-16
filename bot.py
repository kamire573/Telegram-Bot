import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env") 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
  raise ValueError("Bot token not found in .env")
print(TELEGRAM_BOT_TOKEN)

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN
from api_handler import APIHandler

#Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        "Welcome to Camilla's test API Bot! Use:\n"
        "/posts - Here's the recent post\n"
        "/post <id> - Get a specific post by ID\n"
        "/help - Show commands"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n"
        "/posts - Fetch the latest 5 posts\n"
        "/post <id> - Fetch a post by ID (e.g., /post 1)\n"
        "/start - Show welcome message"
    )

async def posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch and display a list of posts with ID, title, & body."""
    result = await APIHandler.get_posts()  
    if result["status"] == "success":
        response = "Latest links:\n"
        for post in result["data"]:
            response += f"ID: {post['id']} - {post['title']}\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Error: {result['message']}")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch and display a specific post by ID."""
    if not context.args:
        await update.message.reply_text("Please provide a link ID (e.g., /link 1)")
        return

    try:
        post_id = int(context.args[0])
        if post_id <= 0:
            raise ValueError("Post ID must be a positive integer")
        
        result = await APIHandler.get_post_by_id(post_id)
        if result["status"] == "success":
            post = result["data"]
            response = "Post {post['id']}:\nTitle: {post['title']}\nBody: {post['body']}"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(f"Error: {result['message']}")
    except ValueError:
        await update.message.reply_text("Invalid post ID. Please use a positive number.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors during bot operation."""
    logger.error(f"Update {update} caused error: {context.error}")
    if update:
        await update.message.reply_text("An error occurred. Please try again later.")

def main() -> None:
    """Run the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env file")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("posts", posts))
    application.add_handler(CommandHandler("post", post))
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()