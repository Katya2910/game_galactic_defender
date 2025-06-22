from dataclasses import dataclass
from .colors import Colors

"""
    # Параметры пули игрока.
"""
@dataclass
class BulletConfig:
    SPEED: int = 10                # Скорость пули
    WIDTH: int = 6                 # Ширина пули
    HEIGHT: int = 16               # Высота пули
    COLOR: tuple = Colors.YELLOW   # Цвет пули
    DAMAGE: int = 1                # Базовый урон 