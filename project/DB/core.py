"""
Основные функции для работы с базой данных
"""
import sqlite3


def get_connection():
    """Возвращает соединение с базой данных"""
    return sqlite3.connect('userdata.db')


def init_db():
    """Инициализирует базу данных, создавая таблицы если их нет"""
    connection = get_connection()
    cursor = connection.cursor()

    # Создаем таблицу пользователей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       username
                       TEXT
                       NOT
                       NULL,
                       everyday_rating
                       INTEGER
                       DEFAULT
                       0,
                       last_problem_rating
                       INTEGER
                       DEFAULT
                       0
                   )
                   ''')

    connection.commit()
    connection.close()


def add_or_update_user(user_id: int, username: str, last_rating: int = 0):
    """
    Добавляет или обновляет пользователя в базе данных

    Args:
        user_id: ID пользователя
        username: Имя пользователя
        last_rating: Последний рейтинг задачи
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO Users (id, username, last_problem_rating) 
        VALUES (?, ?, ?)
    ''', (user_id, username, last_rating))

    connection.commit()
    connection.close()


def get_all_users():
    """
    Возвращает список всех пользователей

    Returns:
        list: Список кортежей с данными пользователей
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM Users")
    users = cursor.fetchall()

    connection.close()
    return users