"""
Модуль для работы с базой данных
"""
from .core import (
    get_connection,
    init_db,
    add_or_update_user,
    get_all_users,
)

# Явно указываем что экспортируем
__all__ = [
    'get_connection',
    'init_db',
    'add_or_update_user',
    'get_all_users',
]