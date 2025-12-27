import random
from VibeCodeBot.project.DB import add_or_update_user
import requests

def get_problem_by_rating(rating: int, user_id: int, username: str) -> str:
    try:
        url = "https://codeforces.com/api/problemset.problems"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            return "Ошибка при получении данных с Codeforces"

        problems = data["result"]["problems"]
        rated_problems = [p for p in problems if p.get("rating") == rating]

        if not rated_problems:
            return f"Нет задач с рейтингом {rating}"

        problem = random.choice(rated_problems)
        contest = problem["contestId"]
        index = problem["index"]
        name = problem["name"]
        link = f"https://codeforces.com/problemset/problem/{contest}/{index}"

        # Используем новый интерфейс для работы с БД
        add_or_update_user(user_id, username, rating)

        return f"🎯 *Задача {contest}{index}: {name}*\n\n🔗 {link}\n\nРейтинг: {rating}"

    except requests.exceptions.RequestException:
        return "Ошибка подключения к Codeforces"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"