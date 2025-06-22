import math
from typing import Tuple
from src.models.movement_patterns.boss_movement_pattern import BossMovementPattern
from src.config.config import Config

class CircularPattern(BossMovementPattern):
    def update(self, timer, current_x, current_y):
        radius = 50
        angle = timer * 0.05
        new_x = int(current_x + math.cos(angle) * radius)
        new_y = int(current_y + math.sin(angle) * radius)
        return new_x, new_y

    def should_switch(self, timer):
        return timer > 100  