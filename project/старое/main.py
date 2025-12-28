import telebot
from telebot import types
from VibeCodeBot.project.services import oldproblem
from admin import admin_panel,broadcast

TOKEN = "7412087237:AAHzrnzI_o2-tE_6VkjE1vJAzbJqwPEUUWk"
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Ссылка на доступ к сайту')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Турниры')
    btn3 = types.KeyboardButton('Моя сегодняшняя задача')
    markup.row(btn2, btn3)

    bot.send_message(
        message.chat.id,
        'Привет! Выбирай то, что тебе нужно:',
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == 'Ссылка на доступ к сайту')
def send_codeforces_link(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Codeforces', url='https://codeforces.com/')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Переходи по ссылке:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Моя сегодняшняя задача')
def daily_problem_handler(message):

    bot.send_message(
        message.chat.id,
        "Введите рейтинг задачи, например: /problem 1000"
    )



@bot.message_handler(commands=["problem"])
def problem_command_handler(message):

    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Использование: /problem <рейтинг>\nПример: /problem 1000")
            return

        rating = int(parts[1])
        if rating % 100 != 0 or rating < 800 or rating > 3500:
            bot.send_message(
                message.chat.id,
                "Рейтинг должен быть кратным 100 и в диапазоне 800-3500\nПример: 800, 900, 1000, ..."
            )
            return

        user_id = message.from_user.id
        username = message.from_user.username or f"user_{user_id}"
        result = oldproblem.get_problem_by_rating(rating, user_id, username)
        bot.send_message(message.chat.id, result, parse_mode="Markdown")

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите число. Например: /problem 1000")

@bot.message_handler(commands=["admin"])
def handle_admin_panel(message):
    admin_panel(message)

@bot.message_handler(commands=["broadcast"])
def handle_broadcast(message):
    broadcast(message)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.text == 'Турниры':
        bot.send_message(message.chat.id, "Функция турниров в разработке 🚧")
    else:
        bot.send_message(message.chat.id, "Используйте кнопки меню или команды")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)