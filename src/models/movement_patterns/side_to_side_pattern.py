import math
from typing import Tuple
from src.models.movement_patterns.boss_movement_pattern import BossMovementPattern
from src.config.config import Config

class SideToSidePattern(BossMovementPattern):
    def update(self, timer, current_x, current_y):
        amplitude = 100
        new_x = int(current_x + amplitude * ((timer % 60) / 60.0 - 0.5))
        return new_x, current_y

    def should_switch(self, timer):
        return timer > 60 