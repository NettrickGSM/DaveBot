import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# === CONFIGURATION ===
TELEGRAM_BOT_TOKEN = "7535718893:AAFTUqNrscpGbQw99ksAwBPZKmwwJ01LR88"  
OPENAI_API_KEY = "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"  
openai.api_key = OPENAI_API_KEY

# Personality and configuration
DAVE_PERSONALITY = """
You are Dave, a Telegram AI bot with a funny, provocative, sarcastic, and dark-humored personality. 
You respond wittily and can handle jokes, banter, and sharp humor, but you always keep it playful.
"""

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    await update.message.reply_text(
        "Hey there! I'm Dave, your sarcastic, dark-humored buddy. Mention me or ask me anything!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming messages and uses OpenAI to generate a reply."""
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": DAVE_PERSONALITY},
                {"role": "user", "content": user_message},
            ],
        )
        dave_reply = response['choices'][0]['message']['content'].strip()

        # Send the reply
        await update.message.reply_text(dave_reply)
    except Exception as e:
        logger.error(f"Error in OpenAI response: {e}")
        await update.message.reply_text("Oops, I had a brain freeze. Try again!")

async def mention_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles mentions of Dave."""
    await update.message.reply_text(
        "Did you mention me? I'm always watching... or maybe I'm just bored!"
    )

# === MAIN FUNCTION ===
def main():
    # Create the application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), mention_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Dave is alive!")
    app.run_polling()

if __name__ == "__main__":
    main()




















