import threading
import telebot
from telebot import types
from telebot.apihelper import copy_message


from VibeCodeBot.config import ADMIN_IDS,BOT_TOKEN
from VibeCodeBot.DB.core import init_db, get_connection
from VibeCodeBot.services.everyday import scheduler_loop
from VibeCodeBot.keyboards.main_menu import admin_menu
from VibeCodeBot.keyboards.main_menu import rating_inline_keyboard, rating_one_keyboard
from VibeCodeBot.handlers.start import (
    start_handler,
    one_callback_handler,
    daily_handler,
    daily_rating_callback,
    daily_done_callback,
    one_done_callback,
)
import sqlite3

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])

def start(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(message.chat.id, "👑 *Админ-панель*\n", reply_markup=admin_menu())
    else:
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


@bot.message_handler(func=lambda m: m.text == "📨Рассылка")
def broadcast(message):
    bot.send_message(message.chat.id, "Введите текст для рассылки:")
    message.text = None
    bot.register_next_step_handler(message, broadcast_next)

def broadcast_next(message):
    broadcast.message = message.text
    text_to_send = broadcast.message
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Users")
    users = cursor.fetchall()
    connection.close()

    bot.send_message(message.chat.id, f"▶ Начинаю рассылку ({len(users)} пользователей)...")

    sent = 0
    blocked = 0

    for user in users:
        user_id = user[0]
        try:
            bot.send_message(user_id, text_to_send)
            sent += 1
        except Exception as e:
            blocked += 1
            print(f"Ошибка отправки пользователю {user_id}: {e}")

    bot.send_message(
        message.chat.id,
        f"✔ Рассылка завершена!\n"
        f"📨 Отправлено: {sent}\n"
        f"⛔ Заблокировали: {blocked}"
    )


@bot.message_handler(func=lambda m: m.text == "🧮Статистика")
def users_stats(message):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT username, month_done FROM Users")
    rows = cur.fetchall()
    if not rows:
        bot.send_message(message.chat.id, "Статистика пользователей:\nПользователей нет.")
        return

    text = "Статистика пользователей:\n" + "\n".join(f"@{uid}: {name}" for uid, name in rows)
    bot.send_message(message.chat.id, text)  # chat_id, text [web:7]
    con.close()

if __name__ == "__main__":
    init_db()
    threading.Thread(target=scheduler_loop, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()
