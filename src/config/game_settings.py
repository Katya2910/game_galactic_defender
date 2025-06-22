from dataclasses import dataclass

"""
    # Основные параметры игры.
"""
@dataclass
class GameSettings:
    SCREEN_WIDTH: int = 1280   # Ширина экрана
    SCREEN_HEIGHT: int = 720   # Высота экрана
    FPS: int = 60              # Кадров в секунду
    BG_COLOR: tuple = (0, 0, 20) # Цвет фона
    MAX_LEVELS: int = 4        # Максимальное количество уровней 