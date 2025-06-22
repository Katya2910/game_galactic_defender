from abc import ABC, abstractmethod
from typing import Tuple

class BossMovementPattern:
    def update(self, timer: int, current_x: int, current_y: int):
        pass
    def should_switch(self, timer: int):
        pass 