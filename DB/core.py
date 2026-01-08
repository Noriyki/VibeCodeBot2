import sqlite3
from VibeCodeBot.DB.models import Users  # или относительный импорт

def get_connection():
    # Можно добавить check_same_thread=False, если будет доступ из разных потоков
    return sqlite3.connect("userdata.db")

def init_db():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(Users.get_table_definition())
        connection.commit()
    finally:
        connection.close()

def add_or_update_user(
    user_id: int,
    username: str,
    everyday_rating: int = 0,
    last_rating: int = 0,
    chat_id: int | None = None,
):
    """
    Обновляем пользователя, не затирая chat_id, если его не передали.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Users (id, username, everyday_rating, last_problem_rating, chat_id)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                everyday_rating = excluded.everyday_rating,
                last_problem_rating = excluded.last_problem_rating,
                chat_id = COALESCE(excluded.chat_id, Users.chat_id)
            """,
            (user_id, username, everyday_rating, last_rating, chat_id),
        )
        connection.commit()
    finally:
        connection.close()

def get_all_users():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Users")
        return cursor.fetchall()
    finally:
        connection.close()
