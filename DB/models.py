"""
Описание моделей базы данных (зарезервировано для будущих улучшений)
"""


class Users:
    """Модель таблицы пользователей"""

    @staticmethod
    def get_table_definition():
        """Возвращает SQL-запрос для создания таблицы"""
        return '''
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
        '''