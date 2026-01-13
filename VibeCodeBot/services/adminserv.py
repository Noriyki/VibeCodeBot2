import threading
import telebot
from telebot import types
from VibeCodeBot.config import BOT_TOKEN

from VibeCodeBot.config import ADMIN_IDS
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
import sqlite3

bot = telebot.TeleBot(BOT_TOKEN)

def user_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Помощь"))
    return kb

def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Статистика"), types.KeyboardButton("Рассылка"))
    kb.add(types.KeyboardButton("Настройки"))
    return kb

