from dataclasses import dataclass

"""Параметры обычного босса."""
@dataclass
class BossConfig:
    SIZE: int = 80                  # Размер босса
    SPAWN_Y: int = -100             # Координата появления по Y
    ATTACK_DELAY: int = 1000        # Задержка между атаками (мс)
    HEALTH_MULTIPLIER: int = 50     # Множитель здоровья
    SPEED_MULTIPLIER: float = 2.0   # Множитель скорости
    ATTACK_COOLDOWN: int = 2000     # Перезарядка атаки (мс)

"""Параметры финального босса."""
@dataclass
class FinalBossConfig:
    SIZE: int = 100
    SPAWN_Y: int = -150
    HEALTH: int = 10
    SCORE: int = 500
    MOVEMENT_SPEED: float = 2.0
    TARGET_Y: int = 100
    MOVEMENT_AMPLITUDE_X: int = 50
    MOVEMENT_AMPLITUDE_Y: int = 30
    MAX_MINI_ENEMIES: int = 100
    SPAWN_DELAY: int = 5000
    SPAWN_BATCH_SIZE: int = 15
    SPAWN_DISTANCE_MIN: int = 50
    SPAWN_DISTANCE_MAX: int = 150
    MINI_ENEMY_SIZE: int = 20
    MINI_ENEMY_SPEED_MULTIPLIER: float = 2.0

"""Параметры мини-босса, который спаунит мини-врагов."""
@dataclass
class MiniSpawnerBossConfig:
    HEALTH_MULTIPLIER: int = 2
    SCORE: int = 200
    MAX_MINI_ENEMIES: int = 30
    SPAWN_DELAY: int = 2000
    SPAWN_OFFSET: int = 50
    MINI_ENEMY_SIZE: int = 20
    MINI_ENEMY_SPEED_MULTIPLIER: float = 1.5 