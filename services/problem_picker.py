import random
import requests
from VibeCodeBot.services.CodeforceApi import get_problems_by_rating
from VibeCodeBot.DB import add_or_update_user



def pick_random_by_rating(rating: int):
    problems = get_problems_by_rating(rating)
    return random.choice(problems) if problems else None


def format_problem(problem: dict) -> str:
    contest = problem.get("contestId", "")
    index = problem.get("index", "")
    name = problem.get("name", "Без названия")
    rating = problem.get("rating", "N/A")
    link = f"https://codeforces.com/problemset/problem/{contest}/{index}"
    return f"🎯 *Задача {contest}{index}: {name}*\n\n🔗 {link}\n\nРейтинг: {rating}"


def get_problem_by_rating(rating: int, user_id: int, username: str) -> str:
    try:
        problem = pick_random_by_rating(rating)
        if not problem:
            return f"Нет задач с рейтингом {rating}"

        add_or_update_user(user_id, username, last_rating=rating)
        return format_problem(problem)

    except requests.exceptions.RequestException:
        return "Ошибка подключения к Codeforces"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
