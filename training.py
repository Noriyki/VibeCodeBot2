import random
import telebot
import requests
import sqlite3
import telebot
from telebot import types
import problem
from telebot.util import user_link

TOKEN = "7412087237:AAHzrnzI_o2-tE_6VkjE1vJAzbJqwPEUUWk"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["training"])
def training(message):
    try:
        parts = message.text.split()

        if len(parts) < 3:
            bot.send_message(message.chat.id, "Использование: /training <рейтинг> <кол-во задач>")
            return

        rating = int(parts[1])
        amount = int(parts[2])

        url = "https://codeforces.com/api/problemset.problems"
        data = requests.get(url).json()
        problems = data["result"]["problems"]

        rated = [p for p in problems if p.get("rating") == rating]

        if not rated:
            bot.send_message(message.chat.id, f"Нет задачи с рейтингом {rating}")
            return

        selected = random.sample(rated, min(amount, len(rated)))

        reply = "Ваша тренировка:\n\n"
        for p in selected:
            contest = p["contestId"]
            index = p["index"]
            name = p["name"]
            link = f"https://codeforces.com/problemset/problem/{contest}/{index}"
            reply += f"🔸 *{name}*\n{link}\n\n"

        bot.send_message(message.chat.id, reply, parse_mode="Markdown")

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректные числа!")

bot.polling(none_stop=True)