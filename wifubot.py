# anime_bot.py
import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменной окружения (безопаснее!)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не задан! Установите переменную TELEGRAM_BOT_TOKEN.")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /waifu, чтобы получить аниме-девочку 💖")

async def waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/waifu")
        resp.raise_for_status()
        url = resp.json().get("url")
        if url:
            await update.message.reply_photo(photo=url)
        else:
            await update.message.reply_text("Не удалось загрузить картинку 😢")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Что-то пошло не так...")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("waifu", waifu))
    print("Бот запускается...")
    app.run_polling()

if __name__ == "__main__":
    main()
