
class Users:
    @staticmethod
    def get_table_definition() -> str:
        return """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            chat_id INTEGER,
            everyday_rating INTEGER DEFAULT 0,
            last_problem_rating INTEGER DEFAULT 0,
            daily_problem_key TEXT,
            daily_date TEXT,
            month_done INTEGER DEFAULT 0,
            month_key TEXT,

            rating_date TEXT
        );
        """
