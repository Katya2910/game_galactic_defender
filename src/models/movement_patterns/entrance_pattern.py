from typing import Tuple
from src.models.movement_patterns.boss_movement_pattern import BossMovementPattern

class EntrancePattern(BossMovementPattern):
    def update(self, timer, current_x, current_y):
        # Медленное движение вниз до y=50
        new_y = current_y + 1
        return current_x, new_y

    def should_switch(self, timer):
        return timer > 50 