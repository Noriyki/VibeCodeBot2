import threading
import telebot
from telebot import types
from services.everyday import scheduler_loop
from VibeCodeBot.config import BOT_TOKEN
from DB.core import init_db
from keyboards.main_menu import rating_inline_keyboard
from handlers.start import (
    start_handler,
    one_handler,
    daily_handler,
    done_handler,
    daily_rating_callback,
    daily_done_callback
)


# ================== CONFIG ==================

bot = telebot.TeleBot(BOT_TOKEN)

# ================== COMMANDS REGISTRATION ==================

@bot.message_handler(commands=['start'])
def handle_sart(message: types.Message):
    start_handler(bot, message)


@bot.message_handler(func=lambda m: m.text == "🎯 Одна задача")
def handle_one(message: types.Message):
    one_handler(bot, message)


@bot.message_handler(func=lambda m: m.text == "⚙️ Задать рейтинг")
def handle_daily_rating(message: types.Message):
    bot.send_message(message.chat.id,
                     "Выберите рейтинг ежедневной задачи:",
                     reply_markup=rating_inline_keyboard())


@bot.callback_query_handler(func=lambda c: c.data.startswith("daily_rating:"))
def handle_daily_rating_callback(call):
    daily_rating_callback(bot, call)


@bot.message_handler(func=lambda m: m.text == "📌 Ежедневная задача")
def handle_daily(message: types.Message):
    daily_handler(bot, message)


@bot.message_handler(func=lambda m: m.text == "✅ Отметить выполненной")
def handle_done(message: types.Message):
    done_handler(bot, message)


@bot.callback_query_handler(func=lambda c: c.data == "daily_done")
def handle_daily_done_callback(call):
    daily_done_callback(bot, call)


# ================== MAIN ==================

if __name__ == "__main__":
    init_db()

    threading.Thread(
        target=scheduler_loop,
        daemon=True
    ).start()

    print("Бот запущен...")
    bot.infinity_polling()
