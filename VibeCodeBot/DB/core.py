import sqlite3


def get_connection():
    return sqlite3.connect("userdata.db")


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
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
        );
        """
    )

    connection.commit()
    connection.close()


def add_or_update_user(
    user_id: int,
    username: str,
    everyday_rating: int | None = None,
    last_rating: int | None = None,
    chat_id: int | None = None,
):
    """
    Вариант 1: без INSERT OR REPLACE.
    Обновляем только те поля, которые переданы, чтобы не затирать everyday_rating.
    """
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
    exists = cur.fetchone() is not None

    if not exists:
        cur.execute(
            """
            INSERT INTO Users (id, username, chat_id, everyday_rating, last_problem_rating)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                chat_id if chat_id is not None else 0,
                everyday_rating if everyday_rating is not None else 0,
                last_rating if last_rating is not None else 0,
            ),
        )
    else:
        # username обновляем всегда (пусть актуализируется)
        cur.execute("UPDATE Users SET username = ? WHERE id = ?", (username, user_id))

        if chat_id is not None:
            cur.execute("UPDATE Users SET chat_id = ? WHERE id = ?", (chat_id, user_id))

        if everyday_rating is not None:
            cur.execute(
                "UPDATE Users SET everyday_rating = ? WHERE id = ?",
                (everyday_rating, user_id),
            )

        if last_rating is not None:
            cur.execute(
                "UPDATE Users SET last_problem_rating = ? WHERE id = ?",
                (last_rating, user_id),
            )

    con.commit()
    con.close()

def get_all_users():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id FROM Users")
    users = cur.fetchall()
    con.close()
    return users
