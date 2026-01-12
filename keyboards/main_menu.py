from telebot import types
from VibeCodeBot.config import RATINGS


def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_daily = types.KeyboardButton("📌 Ежедневная задача")
    btn_one = types.KeyboardButton("🎯 Одна задача")
    btn_rating = types.KeyboardButton("⚙️ Задать рейтинг")

    keyboard.add(btn_daily, btn_one)
    keyboard.add(btn_rating)
    return keyboard


def rating_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(
            text=str(rating),
            callback_data=f"daily_rating:{rating}",
        )
        for rating in RATINGS
    ]
    keyboard.add(*buttons)
    return keyboard


def rating_one_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(
            text=str(rating),
            callback_data=f"one_rating:{rating}",
        )
        for rating in RATINGS
    ]
    keyboard.add(*buttons)
    return keyboard


def daily_done_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="✅ Я решил задачу",
            callback_data="daily_done",
        )
    )
    return keyboard


def one_done_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="✅ Я решил задачу",
            callback_data="one_done",
        )
    )
    return keyboard


def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🧮Статистика"), types.KeyboardButton("📨Рассылка"))

    return kb


