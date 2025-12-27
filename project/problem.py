import requests
from DB import add_or_update_user
from services import pick_random_by_rating, format_problem


def get_problem_by_rating(rating, user_id, username):
    try:
        # Используем новый модуль для выбора задачи
        problem = pick_random_by_rating(rating)

        if not problem:
            return f"Нет задач с рейтингом {rating}"

        # Сохраняем пользователя в БД
        add_or_update_user(user_id, username, rating)

        # Форматируем задачу
        return format_problem(problem)

    except requests.exceptions.RequestException:
        return "Ошибка подключения к Codeforces"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"