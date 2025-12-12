
import sqlite3
from telebot import TeleBot
ADMIN_ID = [1479190231,1162481819,1220983765]

TOKEN = "7412087237:AAHzrnzI_o2-tE_6VkjE1vJAzbJqwPEUUWk"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if not message.from_user.id in ADMIN_ID:
        bot.send_message(message.chat.id, "❌ У вас нет доступа.")
        return

    bot.send_message(
        message.chat.id,
        "👑 *Админ-панель*\n"
        "/broadcast <текст> — отправить сообщение всем пользователям",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["broadcast"])
def broadcast(message):
    if not  message.from_user.id in ADMIN_ID:
        bot.send_message(message.chat.id, "❌ У вас нет доступа.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Использование: /broadcast <текст>")
        return

    text_to_send = parts[1]
    connection = sqlite3.connect('userdata.db')
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