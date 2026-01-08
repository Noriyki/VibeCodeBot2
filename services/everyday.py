import time
import schedule
import telebot
import datetime as dt

from VibeCodeBot.config import BOT_TOKEN, DAILY_TIME
from VibeCodeBot.DB import get_connection, add_or_update_user
from VibeCodeBot.services.problem_picker import pick_random_by_rating, format_problem
from VibeCodeBot.keyboards.main_menu import daily_done_keyboard

bot = telebot.TeleBot(BOT_TOKEN)


def set_daily_rating(user_id: int, username: str, rating: int):
    """Пользователь выбирает рейтинг ежедневной задачи."""
    add_or_update_user(user_id, username, everyday_rating=rating)


def get_daily_problem(user_id: int, username: str) -> tuple[str, bool]:
    """
    Возвращает (text, is_new_today).
    is_new_today=True только если сейчас назначили новую задачу на today.
    """
    today = dt.date.today().isoformat()  # YYYY-MM-DD
    mkey = dt.date.today().strftime("%Y-%m")  # YYYY-MM

    con = get_connection()
    cur = con.cursor()

    # 1) Получаем текущий ежедневный рейтинг
    cur.execute("SELECT everyday_rating FROM Users WHERE id = ?", (user_id,))
    row = cur.fetchone()

    if row is None:
        add_or_update_user(user_id, username, everyday_rating=800, last_rating=0)
        everyday_rating = 800
    else:
        everyday_rating = row[0] or 800

    # 2) Сброс счётчика при смене месяца
    cur.execute("SELECT month_key FROM Users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if not row or row[0] != mkey:
        cur.execute(
            "UPDATE Users SET month_key = ?, month_done = 0 WHERE id = ?",
            (mkey, user_id),
        )

    # 3) Если уже назначена на сегодня — вернуть ту же, но is_new_today=False
    cur.execute(
        "SELECT daily_date, daily_problem_key FROM Users WHERE id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    if row and row[0] == today and row[1]:
        con.commit()
        con.close()
        return f"✅ Ежедневная задача на сегодня уже назначена: *{row[1]}*", False

    # 4) Назначаем новую
    problem = pick_random_by_rating(everyday_rating)
    if not problem:
        con.commit()
        con.close()
        return f"Нет задач с рейтингом {everyday_rating}", False

    daily_key = f"{problem.get('contestId', '')}{problem.get('index', '')}"

    cur.execute(
        "UPDATE Users SET daily_date = ?, daily_problem_key = ?, last_problem_rating = ? WHERE id = ?",
        (today, daily_key, everyday_rating, user_id),
    )

    con.commit()
    con.close()

    return "📌 Ежедневная задача:\n\n" + format_problem(problem), True


# Оставим старое имя, если где-то вызывается
def get_daily_problem_text(user_id: int, username: str) -> str:
    text, _is_new = get_daily_problem(user_id, username)
    return text


def mark_daily_done(user_id: int) -> int:
    """Увеличивает счётчик выполненных задач за текущий месяц и возвращает значение."""
    mkey = dt.date.today().strftime("%Y-%m")

    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT month_key, month_done FROM Users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        con.close()
        return 0

    month_key, month_done = row
    if month_key != mkey:
        month_done = 0
        month_key = mkey

    month_done += 1
    cur.execute(
        "UPDATE Users SET month_key = ?, month_done = ? WHERE id = ?",
        (month_key, month_done, user_id),
    )

    con.commit()
    con.close()
    return month_done


# ================== DAILY SCHEDULER ==================

def send_daily_to_all_users():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, username, chat_id FROM Users WHERE chat_id IS NOT NULL AND chat_id != 0")
    users = cur.fetchall()
    con.close()

    for user_id, username, chat_id in users:
        try:
            text, is_new = get_daily_problem(user_id, username)

            # 1) Защита от повторной отправки: если задача уже была назначена сегодня, не шлём
            if not is_new:
                continue

            # 2) В рассылке добавляем кнопку "выполнил"
            bot.send_message(chat_id, text, reply_markup=daily_done_keyboard())

        except Exception as e:
            print(f"Не удалось отправить {user_id}: {e}")


def scheduler_loop():
    schedule.every().day.at(DAILY_TIME).do(send_daily_to_all_users)
    while True:
        schedule.run_pending()
        time.sleep(1)
