from dataclasses import dataclass

"""
    # Параметры движения врагов и боссов.
"""
@dataclass
class MovementConfig:
    SEED_RANGE: int = 1000000  # Диапазон для генерации seed
    TIME_RANGE: int = 1000     # Диапазон времени для паттернов
    DIRECTION_CHANGE_MIN: int = 60  # Минимальная частота смены направления
    DIRECTION_CHANGE_MAX: int = 180 # Максимальная частота смены направления
    BASE_FREQ: float = 0.01         # Базовая частота шума
    FREQ_INCREMENT: float = 0.005   # Прирост частоты
    BASE_SCALE: float = 1.0         # Базовый масштаб
    SCALE_INCREMENT: float = 0.5    # Прирост масштаба 