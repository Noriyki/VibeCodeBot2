import sqlite3
from contextlib import contextmanager
from typing import List, Optional
from .models import User

DATABASE_NAME = 'userdata.db'

@contextmanager
def get_connection():
    """Контекстный менеджер для работы с БД"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы получать данные как словари
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Инициализация таблиц"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           everyday_rating INTEGER DEFAULT 0,
           last_problem_rating INTEGER DEFAULT 0
            )
                ''')
