
import requests


def get_all_problems():
    """Получает все задачи с Codeforces"""
    try:
        url = "https://codeforces.com/api/problemset.problems"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            return None

        return data["result"]
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


def get_problems_by_rating(rating):

    data = get_all_problems()
    if not data:
        return []

    problems = data["problems"]
    # Фильтруем задачи по рейтингу (как в оригинальном problem.py)
    return [p for p in problems if p.get("rating") == rating]