
import random


def pick_random_by_rating(rating):

    from cf_api import get_problems_by_rating

    problems = get_problems_by_rating(rating)
    return random.choice(problems) if problems else None


def pick_multiple_by_rating(rating, amount):

    from cf_api import get_problems_by_rating

    problems = get_problems_by_rating(rating)

    if not problems:
        return []

    # Проверяем, что amount не превышает количество доступных задач
    if amount >= len(problems):
        # Если запросили больше или равно, чем есть, перемешиваем и возвращаем все
        random.shuffle(problems)
        return problems
    else:
        # Иначе выбираем случайные задачи
        return random.sample(problems, amount)


def format_problem(problem):
    contest = problem.get("contestId", "")
    index = problem.get("index", "")
    name = problem.get("name", "Без названия")
    rating = problem.get("rating", "N/A")

    link = f"https://codeforces.com/problemset/problem/{contest}/{index}"

    # Форматирование как в оригинальном problem.py
    return f"🎯 *Задача {contest}{index}: {name}*\n\n🔗 {link}\n\nРейтинг: {rating}"