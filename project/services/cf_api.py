def get_all_problems():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url, timeout=10)
    data = response.json()
    if data["status"] == "OK":
        return data["result"]["problems"]
    return []

def get_problems_by_rating(rating):
    problems = get_all_problems()
    return [p for p in problems if p.get("rating") == rating]