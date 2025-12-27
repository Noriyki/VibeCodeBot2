# database/models.py

from dataclasses import dataclass

@dataclass
class User:

    id: int
    username: str
    last_problem_rating: int = 0