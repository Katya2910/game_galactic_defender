import pygame
import random
from src.models.boss import Boss
from src.models.enemy import Enemy
from src.config.config import Config
from src.utils.enums import Difficulty

"""
    # Класс мини-босса, который периодически спаунит мини-врагов вокруг себя.
"""
class MiniSpawnerBoss(Boss):
    def __init__(self, difficulty: Difficulty):
        super().__init__(difficulty)
        
        self.health = difficulty.value["boss_health"] * 2  # Увеличенное здоровье
        self.max_health = self.health
        self.score_value = 200 * difficulty.value["score_multiplier"]
        
        self.max_mini_enemies = 30  # Максимум мини-врагов
        self.mini_enemies_spawned = 0
        self.spawn_delay = 2000     # Задержка между спавнами (мс)
        self.last_spawn_time = 0

    def update(self, player_pos: tuple[int, int] = None) -> None:
        """Обновляет состояние мини-босса и спаунит мини-врагов по таймеру."""
        super().update(player_pos)
        
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_spawn_time >= self.spawn_delay and 
            self.mini_enemies_spawned < self.max_mini_enemies):
            self.spawn_mini_enemy()
            self.last_spawn_time = current_time

    def spawn_mini_enemy(self) -> None:
        """Создаёт мини-врага рядом с боссом, если не превышен лимит."""
        if self.mini_enemies_spawned >= self.max_mini_enemies:
            return
            
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        
        mini_enemy = Enemy(self.difficulty, level=1) 
        mini_enemy.rect.x = self.rect.x + offset_x
        mini_enemy.rect.y = self.rect.y + offset_y
        
        # Уменьшаем размер мини-врага
        mini_enemy.rect.width = 20
        mini_enemy.rect.height = 20
        mini_enemy.image = pygame.transform.scale(mini_enemy.image, (20, 20))
        mini_enemy.health = 1
        mini_enemy.max_health = 1
        
        # Увеличиваем скорость мини-врага
        mini_enemy.speed *= 1.5
        
        self.mini_enemies_spawned += 1 