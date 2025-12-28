
import time
import threading
import schedule
import telebot
from telebot import types
from dotenv import load_dotenv
import os
load_dotenv()
from services.everyday import (
    set_daily_rating,
    get_daily_problem_text,
    mark_daily_done,
)
from services.problem_picker import get_problem_by_rating
from DB.core import init_db, add_or_update_user, get_connection


# ================== CONFIG ==================

BOT_TOKEN = os.getenv("BOT_TOKEN")
DAILY_TIME = "09:00"

bot = telebot.TeleBot(BOT_TOKEN)


# ================== HELPERS ==================

def get_user_data(message: types.Message):
    user_id = message.from_user.id
    username = (
        message.from_user.username
        or message.from_user.first_name
        or "user"
    )
    chat_id = message.chat.id
    return user_id, username, chat_id


def remember_chat(message: types.Message):
    """Сохраняем chat_id для авторассылки."""
    user_id, username, chat_id = get_user_data(message)
    try:
        add_or_update_user(user_id, username, chat_id=chat_id)
    except TypeError:
        pass


def safe_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None


# ================== DAILY SCHEDULER ==================

def send_daily_to_all_users():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, username, chat_id FROM Users WHERE chat_id IS NOT NULL")
    users = cur.fetchall()
    con.close()

    for user_id, username, chat_id in users:
        try:
            text = get_daily_problem_text(user_id, username)
            bot.send_message(chat_id, text)
        except Exception as e:
            print(f"Не удалось отправить {user_id}: {e}")


def scheduler_loop():
    schedule.every().day.at(DAILY_TIME).do(send_daily_to_all_users)

    while True:
        schedule.run_pending()
        time.sleep(1)


# ================== COMMANDS ==================

@bot.message_handler(commands=["start", "help"])
def start(message: types.Message):
    remember_chat(message)
    bot.reply_to(
        message,
        "Команды:\n"
        "/one <rating>\n"
        "/daily_rating <rating>\n"
        "/daily\n"
        "/done"
    )


@bot.message_handler(commands=["one"])
def one(message: types.Message):
    remember_chat(message)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Использование: /one <rating>")
        return

    rating = safe_int(parts[1])
    if rating is None:
        bot.reply_to(message, "Рейтинг должен быть числом")
        return

    user_id, username, chat_id = get_user_data(message)
    text = get_problem_by_rating(rating, user_id, username)
    bot.send_message(chat_id, text)


@bot.message_handler(commands=["daily_rating"])
def daily_rating(message: types.Message):
    remember_chat(message)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Использование: /daily_rating <rating>")
        return

    rating = safe_int(parts[1])
    if rating is None:
        bot.reply_to(message, "Рейтинг должен быть числом")
        return

    user_id, username, _ = get_user_data(message)
    set_daily_rating(user_id, username, rating)
    bot.reply_to(message, f"Ок. Ежедневный рейтинг: {rating}")


@bot.message_handler(commands=["daily"])
def daily(message: types.Message):
    remember_chat(message)
    user_id, username, chat_id = get_user_data(message)
    bot.send_message(chat_id, get_daily_problem_text(user_id, username))


@bot.message_handler(commands=["done"])
def done(message: types.Message):
    remember_chat(message)
    user_id, _, _ = get_user_data(message)
    count = mark_daily_done(user_id)
    bot.reply_to(message, f"Засчитано! В этом месяце: {count}")


# ================== MAIN ==================

if __name__ == "__main__":
    init_db()

    threading.Thread(
        target=scheduler_loop,
        daemon=True
    ).start()

    print("Бот запущен...")
    bot.infinity_polling()
