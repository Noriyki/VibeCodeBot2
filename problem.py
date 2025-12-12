import random
import requests
import sqlite3


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

        connection = sqlite3.connect('userdata.db')
        cursor = connection.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO Users (id, username, last_problem_rating) 
            VALUES (?, ?, ?)
        ''', (user_id, username, rating))

        connection.commit()
        connection.close()

        return f"🎯 *Задача {contest}{index}: {name}*\n\n🔗 {link}\n\nРейтинг: {rating}"

    except requests.exceptions.RequestException:
        return "Ошибка подключения к Codeforces"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"