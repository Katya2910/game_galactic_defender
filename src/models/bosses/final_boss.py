import pygame
import random
import math
from src.models.boss import Boss
from src.models.enemy import Enemy
from src.config.config import Config
from src.utils.enums import Difficulty

"""
    # Финальный босс
"""
class FinalBoss(Boss):
    def __init__(self, difficulty: Difficulty):

        super().__init__(difficulty)
        
        self.health = 10  
        self.max_health = self.health
        self.score_value = 500 * difficulty.value["score_multiplier"]

        boss_image = pygame.image.load("src/assets/images/enemies/enemy_level_3_boss.png")
        boss_image = pygame.transform.scale(boss_image, (100, 100))
        self.image = boss_image


        self.rect.width = 100
        self.rect.height = 100
        
        self.rect.centerx = Config.SCREEN_WIDTH // 2
        self.rect.y = -150
        
        self.movement_time = 0
        self.movement_speed = 2
        self.target_x = Config.SCREEN_WIDTH // 2
        self.target_y = 100
        self.arrived = False
        
        self.mini_enemies_spawned = 0
        self.max_mini_enemies = 100  
        self.spawn_delay = 5000  
        self.last_spawn_time = 0
        self.mini_enemies = pygame.sprite.Group() 
        
    def update(self, player_pos: tuple[int, int] = None) -> None:

        if not self.arrived:
            dx = self.target_x - self.rect.centerx
            dy = self.target_y - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.movement_speed:
                self.rect.centerx = self.target_x
                self.rect.centery = self.target_y
                self.arrived = True
            else:
                self.rect.centerx += (dx/distance) * self.movement_speed
                self.rect.centery += (dy/distance) * self.movement_speed
        else:
            self.movement_time += 0.02
            self.rect.centerx = self.target_x + math.sin(self.movement_time) * 50
            self.rect.centery = self.target_y + math.cos(self.movement_time * 0.5) * 30
        
        self.mini_enemies.update(player_pos)
        
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_spawn_time >= self.spawn_delay and 
            self.mini_enemies_spawned < self.max_mini_enemies):
            self.spawn_mini_enemies()
            self.last_spawn_time = current_time
        
    def spawn_mini_enemies(self) -> None:
        if self.mini_enemies_spawned >= self.max_mini_enemies:
            return
        enemies_to_spawn = min(15, self.max_mini_enemies - self.mini_enemies_spawned)
        i = 0
        while i < enemies_to_spawn:
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(50, 150)
            spawn_x = self.rect.centerx + distance * math.cos(angle)
            spawn_y = self.rect.centery + distance * math.sin(angle)
            mini_enemy = Enemy(self.difficulty, level=1)
            mini_enemy.rect.centerx = spawn_x
            mini_enemy.rect.centery = spawn_y
            mini_enemy.rect.width = 20
            mini_enemy.rect.height = 20
            mini_enemy.image = pygame.transform.scale(mini_enemy.image, (20, 20))
            mini_enemy.speed *= 2.0
            mini_enemy.is_mini_enemy = True
            self.mini_enemies.add(mini_enemy)
            self.mini_enemies_spawned += 1
            i += 1
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        
        self.mini_enemies.draw(screen)
        
        bg_rect = pygame.Rect(
            self.rect.x,
            self.rect.y - 15,
            self.rect.width,
            10
        )
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        segment_width = self.rect.width / self.max_health
        for i in range(self.health):
            segment_rect = pygame.Rect(
                self.rect.x + (i * segment_width),
                self.rect.y - 15,
                segment_width - 2, 
                10
            )
            pygame.draw.rect(screen, Config.GREEN, segment_rect)
        
        pygame.draw.rect(screen, Config.WHITE, bg_rect, 1)
        
        font = pygame.font.Font(None, 24)
        hits_text = font.render(f"Попаданий: {self.health}/{self.max_health}", True, Config.WHITE)
        text_rect = hits_text.get_rect(centerx=self.rect.centerx, top=self.rect.y - 35)
        screen.blit(hits_text, text_rect) 