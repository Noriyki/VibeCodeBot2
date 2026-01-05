
import sqlite3


def get_connection():
    return sqlite3.connect('userdata.db')


def init_db():

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    chat_id INTEGER DEFAULT 0,
    everyday_rating INTEGER DEFAULT 0,
    last_problem_rating INTEGER DEFAULT 0,
    daily_problem_key TEXT,
    daily_date TEXT,
    month_done INTEGER DEFAULT 0,
    month_key TEXT
    )
""")


    connection.commit()
    connection.close()


def add_or_update_user(user_id: int, username: str, everyday_rating:int =  0, last_rating:int = 0):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO Users (id, username, everyday_rating, last_problem_rating) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, everyday_rating, last_rating))

    connection.commit()
    connection.close()


def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM Users")
    users = cursor.fetchall()

    connection.close()
    return users