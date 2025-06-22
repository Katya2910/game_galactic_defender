from dataclasses import dataclass

"""
    # Параметры урона и бонусов в бою.
"""
@dataclass
class CombatConfig:
    COLLISION_DAMAGE: int = 20  # Урон при столкновении
    PLAYER_ENEMY_COLLISION_DAMAGE: int = 10  # Урон игроку при столкновении с врагом
    ENEMY_PLAYER_COLLISION_DAMAGE: int = 20  # Урон врагу при столкновении с игроком
    BOSS_PLAYER_COLLISION_DAMAGE: int = 20   # Урон игроку при столкновении с боссом
    HEALTH_PICKUP_AMOUNT: int = 20           # Количество здоровья при подборе аптечки
    ENEMY_LEVEL2_BONUS_SCORE: int = 20      # Бонусные очки за врага 2 уровня 