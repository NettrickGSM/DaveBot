import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import Dispatcher
import openai
from flask import Flask, request

# Your API keys
TELEGRAM_BOT_TOKEN = "7535718893:AAFTUqNrscpGbQw99ksAwBPZKmwwJ01LR88"
OPENAI_API_KEY = "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"

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app for webhook
app = Flask(__name__)

# Dave's personality
PERSONALITY = "Dave is bratty, dark-humored, provocative, a little racist, and funny. He learns from conversations."

# Define handlers for commands and messages
def handle_dave(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_input_cleaned = user_input.replace("/Dave", "").strip()

    try:
        # Send input to OpenAI and get a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Dave's personality: {PERSONALITY}\nUser said: {user_input_cleaned}\nDave responds:",
            max_tokens=150,
            temperature=0.8,
        )
        bot_reply = response["choices"][0]["text"].strip()
        update.message.reply_text(bot_reply)
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("Dave is too annoyed to reply right now. Try again later.")

def handle_continuation(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    try:
        # Send input to OpenAI and get a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Dave's personality: {PERSONALITY}\nUser continued: {user_input}\nDave responds:",
            max_tokens=150,
            temperature=0.8,
        )
        bot_reply = response["choices"][0]["text"].strip()
        update.message.reply_text(bot_reply)
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("Dave doesn't feel like talking right now.")

# Webhook route for Telegram
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook() -> str:
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    # Initialize the bot and dispatcher
    from telegram import Bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0)

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("Dave", handle_dave))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_continuation))

    # Set webhook
    webhook_url = f"https://nettrick.eu.pythonanywhere.com/<your-bot-token>"  # Replace with your domain
    bot.set_webhook(url=webhook_url)

    # Run Flask app
    app.run(host="0.0.0.0", port=8443)
