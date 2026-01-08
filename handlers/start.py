from telebot import types

from VibeCodeBot.DB.core import add_or_update_user
from VibeCodeBot.services.everyday import (
    set_daily_rating,
    get_daily_problem_text,
    mark_daily_done,
)
from VibeCodeBot.services.problem_picker import get_problem_by_rating
from VibeCodeBot.keyboards.main_menu import main_menu_keyboard, daily_done_keyboard

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
    # здесь важно, чтобы add_or_update_user принимал chat_id
    add_or_update_user(user_id, username, chat_id=chat_id)

def safe_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None

# ================== CALLBACKS ==================

def daily_rating_callback(bot, call: types.CallbackQuery):
    _, rating_str = call.data.split(":")
    rating = int(rating_str)

    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name or "user"

    set_daily_rating(user_id, username, rating)

    bot.answer_callback_query(
        call.id,
        text=f"Ежедневный рейтинг установлен: {rating}",
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Ежедневный рейтинг: {rating}",
    )

def daily_done_callback(bot, call: types.CallbackQuery):
    user_id = call.from_user.id
    # username не используется, можно убрать, но оставлю для будущих расширений
    _username = call.from_user.username or call.from_user.first_name or "user"

    count = mark_daily_done(user_id)

    bot.answer_callback_query(
        call.id,
        text="Задача засчитана 👍",
    )

    new_text = (
        "📌 Ежедневная задача\n\n"
        "✅ Выполнено!\n"
        f"📊 В этом месяце: {count}"
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,  # убираем кнопку
    )

# ================== COMMAND HANDLERS ==================

def start_handler(bot, message: types.Message):
    remember_chat(message)
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=main_menu_keyboard(),
    )

def one_callback_handler(bot, call: types.CallbackQuery):
    remember_chat(call.message)

    _, rating_str = call.data.split(":", 1)
    rating = safe_int(rating_str)
    if rating is None:
        bot.send_message(call.message.chat.id, "Рейтинг должен быть числом")
        return

    user_id, username, chat_id = get_user_data(call.message)
    text = get_problem_by_rating(rating, user_id, username)
    bot.send_message(chat_id, text)

# Эти хендлеры сейчас, похоже, не используются, но можно оставить для /команд

def daily_rating_handler(bot, message: types.Message):
    remember_chat(message)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Использование: /daily_rating <рейтинг>")
        return

    rating = safe_int(parts[1])
    if rating is None:
        bot.reply_to(message, "Рейтинг должен быть числом")
        return

    user_id, username, _ = get_user_data(message)
    set_daily_rating(user_id, username, rating)
    bot.reply_to(message, f"Ок. Ежедневный рейтинг: {rating}")

def daily_handler(bot, message: types.Message):
    remember_chat(message)
    user_id, username, chat_id = get_user_data(message)
    text = get_daily_problem_text(user_id, username)
    bot.send_message(
        chat_id,
        text,
        reply_markup=daily_done_keyboard(),
    )

def done_handler(bot, message: types.Message):
    remember_chat(message)
    user_id, _, _ = get_user_data(message)
    count = mark_daily_done(user_id)
    bot.reply_to(message, f"Засчитано! В этом месяце: {count}")
