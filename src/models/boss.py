import pygame
import math
from src.models.enemy import Enemy
from src.config.config import Config
from src.utils.enums import Difficulty
from src.models.movement_patterns.boss_movement_pattern import BossMovementPattern
from src.models.movement_patterns.entrance_pattern import EntrancePattern
from src.models.movement_patterns.side_to_side_pattern import SideToSidePattern
from src.models.movement_patterns.circular_pattern import CircularPattern

"""
   # Босс: паттерны движения и атака
"""
class Boss(Enemy):
    def __init__(self, difficulty: Difficulty):
        spawn_x = Config.SCREEN_WIDTH // 2 - 40
        spawn_y = -100
        super().__init__(difficulty, level=2)
        self.image = pygame.Surface((80, 80))
        self.image.fill(Config.PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.health = difficulty.value["boss_health"]
        self.max_health = self.health
        self.score_value = 100 * difficulty.value["score_multiplier"]
        self.movement_patterns = [EntrancePattern(), SideToSidePattern(), CircularPattern()]
        self.current_pattern = 0
        self.pattern_timer = 0
        self.attack_timer = 0
        self.attack_delay = 1000

    def update(self, player_pos: tuple[int, int] = None) -> None:
        self.pattern_timer += 1
        self.attack_timer += 1000 / Config.FPS
        pattern = self.movement_patterns[self.current_pattern]
        new_pos = pattern.update(self.pattern_timer, self.rect.x, self.rect.y)
        self.rect.x, self.rect.y = new_pos
        if pattern.should_switch(self.pattern_timer):
            self.switch_pattern()

    def switch_pattern(self) -> None:
        self.current_pattern = self.current_pattern + 1
        if self.current_pattern >= len(self.movement_patterns):
            self.current_pattern = 0
        self.pattern_timer = 0

    def should_attack(self) -> bool:
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0
            return True
        return False 