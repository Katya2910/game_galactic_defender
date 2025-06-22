from enum import Enum
"""
    # Модуль с перечислениями для уровней сложности и состояний игры
"""
class Difficulty(Enum):
    # Уровни сложности игры
    EASY = {
        "enemies": 5,              # Количество врагов
        "enemy_speed": 0.8,        # Скорость врагов
        "enemy_health": 1,         # Здоровье врагов
        "boss_health": 50,         # Здоровье босса
        "score_multiplier": 1,     # Множитель очков
        "name": "Легко"            # Название
    }
    NORMAL = {
        "enemies": 8,
        "enemy_speed": 1.2,
        "enemy_health": 2,
        "boss_health": 100,
        "score_multiplier": 2,
        "name": "Нормально"
    }
    HARD = {
        "enemies": 12,
        "enemy_speed": 1.5,
        "enemy_health": 3,
        "boss_health": 150,
        "score_multiplier": 3,
        "name": "Сложно"
    }

class GameState(Enum):
    # Возможные состояния игры
    MENU = "menu"         # Главное меню
    GAME = "game"         # Игра
    GAME_OVER = "game_over" # Поражение
    VICTORY = "victory"   # Победа
    STORY = "story"       # Сюжет