import threading
import telebot
from telebot import types

from VibeCodeBot.config import BOT_TOKEN
from VibeCodeBot.DB.core import init_db
from VibeCodeBot.services.everyday import scheduler_loop
from VibeCodeBot.keyboards.main_menu import rating_inline_keyboard, rating_one_keyboard
from VibeCodeBot.handlers.start import (
    start_handler,
    one_callback_handler,
    daily_handler,
    daily_rating_callback,
    daily_done_callback,
    one_done_callback,
)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message: types.Message):
    start_handler(bot, message)


@bot.message_handler(func=lambda m: m.text == "🎯 Одна задача")
def handle_one(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Выберите рейтинг для задачи:",
        reply_markup=rating_one_keyboard(),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("one_rating:"))
def handle_one_rating_callback(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    one_callback_handler(bot, call)


@bot.callback_query_handler(func=lambda c: c.data == "one_done")
def handle_one_done_callback(call: types.CallbackQuery):
    one_done_callback(bot, call)


@bot.message_handler(func=lambda m: m.text == "⚙️ Задать рейтинг")
def handle_daily_rating(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Выберите рейтинг ежедневной задачи:",
        reply_markup=rating_inline_keyboard(),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("daily_rating:"))
def handle_daily_rating_callback(call: types.CallbackQuery):
    daily_rating_callback(bot, call)


@bot.message_handler(func=lambda m: m.text == "📌 Ежедневная задача")
def handle_daily(message: types.Message):
    daily_handler(bot, message)


@bot.callback_query_handler(func=lambda c: c.data == "daily_done")
def handle_daily_done_callback(call: types.CallbackQuery):
    daily_done_callback(bot, call)


if __name__ == "__main__":
    init_db()
    threading.Thread(target=scheduler_loop, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()
