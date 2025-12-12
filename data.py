import sqlite3


def init_db():
    connection = sqlite3.connect('userdata.db')
    cursor = connection.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Users (
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           everyday_rating INTEGER DEFAULT 0,
           last_problem_rating INTEGER DEFAULT 0
       )
       ''')

    connection.commit()
    connection.close()


# Инициализируем БД при импорте
init_db()