from dataclasses import dataclass

"""
    # Настройки игрока.
"""
@dataclass
class PlayerConfig:
    SPEED: int = 5              # Скорость игрока
    WIDTH: int = 50             # Ширина спрайта игрока
    HEIGHT: int = 40            # Высота спрайта игрока
    MAX_HEALTH: int = 100       # Максимальное здоровье
    SHOOT_DELAY: int = 250      # Задержка между выстрелами (мс)
    IMAGE_SCALE: float = 1.5    # Масштаб изображения
    IMAGE_WIDTH: int = 75       # Ширина изображения
    IMAGE_HEIGHT: int = 60      # Высота изображения 