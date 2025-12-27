def pick_random_by_rating(rating):
    problems = cf_api.get_problems_by_rating(rating)
    return random.choice(problems) if problems else None

def pick_multiple_by_rating(rating, amount):
    problems = cf_api.get_problems_by_rating(rating)
    return random.sample(problems, min(amount, len(problems)))

def format_problem(problem):
    # Форматирование задачи в Markdown
    return f"🎯 *{problem['name']}*\n🔗 https://codeforces.com/..."