# bot.py
from telegram.ext import Application
from handlers import start, button_callback
from config import BOT_TOKEN
from logger import setup_logger

logger = setup_logger()

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()

        # Регистрация обработчиков
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_callback))

        logger.info("Bot started.")
        app.run_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()