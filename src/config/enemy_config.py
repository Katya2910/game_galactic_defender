from dataclasses import dataclass
from .game_settings import GameSettings

"""
    # Параметры врагов для разных уровней сложности и паттернов поведения.
"""
@dataclass
class EnemyConfig:
    SPAWN_Y_MIN: int = -200            # Минимальная координата появления по Y
    SPAWN_Y_MAX: int = -50             # Максимальная координата появления по Y
    SIZE: int = 30                     # Размер врага
    IMAGE_SCALE: int = 54              # Масштаб изображения врага
    SPAWN_RATE: int = 30               # Частота появления врагов

    PATROL_RADIUS: int = 150           # Радиус патрулирования
    VISION_RANGE: int = 400            # Дальность видимости
    RETREAT_DISTANCE: int = 150        # Дистанция отступления
    BASE_SPEED: float = 2.5            # Базовая скорость
    SPEED_INCREMENT: float = 0.2       # Прирост скорости
    
    LEVEL1_HEALTH: int = 1             # Здоровье врага 1 уровня
    LEVEL2_HEALTH: int = 2             # Здоровье врага 2 уровня
    BASE_SCORE: int = 10               # Базовые очки за врага
    
    STUCK_TIMER: int = 30              # Таймер застревания
    PATH_UPDATE_DELAY: int = 60        # Задержка обновления пути
    ATTACK_DELAY_MIN: int = 1000       # Минимальная задержка атаки (мс)
    ATTACK_DELAY_MAX: int = 2000       # Максимальная задержка атаки (мс)
    
    CHARGE_SPEED_MULTIPLIER: float = 2.0   # Множитель скорости для рывка
    ZIGZAG_AMPLITUDE: int = 50             # Амплитуда зигзага
    ZIGZAG_FREQUENCY: float = 0.05         # Частота зигзага
    CIRCLE_RADIUS: int = 150               # Радиус кругового движения
    CIRCLE_SPEED: float = 0.02             # Скорость кругового движения
    
    COVER_POINTS: list = None              # Точки укрытий
    
    def __post_init__(self):
        """Инициализация точек укрытий по умолчанию."""
        if self.COVER_POINTS is None:
            self.COVER_POINTS = [
                (50, 50), (GameSettings.SCREEN_WIDTH - 50, 50),
                (50, GameSettings.SCREEN_HEIGHT - 50), (GameSettings.SCREEN_WIDTH - 50, GameSettings.SCREEN_HEIGHT - 50)
            ] 