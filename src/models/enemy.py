from typing import List, Optional, Tuple
import pygame
import random
import math
from src.models.entity import Entity
from src.config.config import Config
from src.utils.enums import Difficulty
from src.utils.perlin_noise import PerlinNoise, EnhancedMovementNoise
from src.utils.pathfinding import ThetaStar
"""
    # Класс врага. Реализует паттерны движения, атаки и взаимодействие с игроком.
"""
class Enemy(Entity):
    def __init__(self, difficulty: Difficulty, level: int = 1):

        spawn_y = random.randint(-200, -50)
        spawn_x = random.randint(0, Config.SCREEN_WIDTH - 30)
        
        super().__init__(
            spawn_x,
            spawn_y,
            30, 30,
            Config.RED if level == 1 else Config.PURPLE
        )
        
        if level == 1:
            enemy_image = pygame.image.load(Config.ENEMY_LEVEL1_IMAGE)
            enemy_image = pygame.transform.scale(enemy_image, (54, 54))
            self.image = enemy_image
            self.rect = self.image.get_rect()
            self.rect.x = spawn_x
            self.rect.y = spawn_y
        else:
            enemy_image = pygame.image.load("src/assets/images/enemies/enemy_level_2.png")
            enemy_image = pygame.transform.scale(enemy_image, (54, 54))
            self.image = enemy_image
            self.rect = self.image.get_rect()
            self.rect.x = spawn_x
            self.rect.y = spawn_y
        self.difficulty = difficulty
        self.speed = difficulty.value["enemy_speed"]
        self.health = 1 if level == 1 else 2
        self.max_health = self.health
        self.score_value = 10 * difficulty.value["score_multiplier"]
        self.level = level

        self.movement_noise = EnhancedMovementNoise(random.randint(0, 1000000))
        self.time = random.random() * 1000
        
        self.pathfinder = ThetaStar((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.current_path = []
        self.path_index = 0
        self.path_update_timer = 0
        self.path_update_delay = 60
        
        self.state = "patrol"
        self.target_position = None
        self.stuck_timer = 0
        self.last_position = (self.rect.x, self.rect.y)
        self.movement_direction = (0, 1)
        
        if level == 3:
            self.formation_position = None
            self.formation_angle = 0
            self.attack_pattern = random.choice(['circle', 'zigzag', 'charge', 'tactical'])
            self.attack_timer = 0
            self.attack_delay = random.randint(1000, 2000)
            self.charge_speed = self.speed * 2
            self.zigzag_amplitude = 50
            self.zigzag_frequency = 0.05
            self.circle_radius = 150
            self.circle_speed = 0.02
            self.tactical_cover_positions = []
        self._set_new_patrol_point()

    def _set_new_patrol_point(self) -> None:
        """
Устанавливает новую точку патрулирования для врага.
"""
        self.target_position = (
            random.randint(0, Config.SCREEN_WIDTH - self.rect.width),
            random.randint(50, Config.SCREEN_HEIGHT - 100)
        )
        dx = self.target_position[0] - self.rect.x
        dy = self.target_position[1] - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.movement_direction = (dx/distance, dy/distance)

    def update(self, player_pos: tuple[int, int] = None) -> None:
        """
Обновляет состояние врага: движение, паттерны, поведение.
"""
        self.movement_noise.update()
        
        current_pos = (self.rect.x, self.rect.y)
        if current_pos == self.last_position:
            self.stuck_timer += 1
            if self.stuck_timer > 30:
                self._set_new_patrol_point()
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0
        self.last_position = current_pos

        if self.rect.top < 0:
            self.rect.y += self.speed
            return

        if self.level == 3 and player_pos:
            self._update_level_3(player_pos)
        else:
            noise_x, noise_y = self.movement_noise.get_movement_offset(
                self.movement_direction, self.speed, self.level
            )
            self.rect.x += self.movement_direction[0] * self.speed + noise_x
            self.rect.y += self.movement_direction[1] * self.speed + noise_y
            self.rect.x = max(0, min(Config.SCREEN_WIDTH - self.rect.width, self.rect.x))
            self.rect.y = max(0, min(Config.SCREEN_HEIGHT - self.rect.height, self.rect.y))
            self.time += 1
            if self.rect.top > Config.SCREEN_HEIGHT:
                self.kill()
                return

    def _update_level_3(self, player_pos: tuple[int, int]) -> None:
        """
Обновляет поведение врага 3 уровня (особые паттерны атаки).
"""
        self.attack_timer += 1
        
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0
            self.attack_pattern = random.choice(['circle', 'zigzag', 'charge', 'tactical'])
        
        if self.attack_pattern == 'circle':
            self._circle_attack(player_pos)
        elif self.attack_pattern == 'zigzag':
            self._zigzag_attack(player_pos)
        elif self.attack_pattern == 'tactical':
            self._tactical_attack(player_pos)
        else:
            self._charge_attack(player_pos)

    def _circle_attack(self, player_pos: tuple[int, int]) -> None:
        """
Реализует круговой паттерн атаки вокруг игрока.
"""
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)
        
        self.formation_angle += self.circle_speed
        target_x = player_pos[0] + math.cos(self.formation_angle) * self.circle_radius
        target_y = player_pos[1] + math.sin(self.formation_angle) * self.circle_radius
        
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.movement_direction = (dx/distance, dy/distance)

    def _zigzag_attack(self, player_pos: tuple[int, int]) -> None:
        """
Реализует зигзагообразный паттерн атаки на игрока.
"""
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            zigzag_offset = math.sin(self.time * self.zigzag_frequency) * self.zigzag_amplitude
            perpendicular_dx = -dy / distance
            perpendicular_dy = dx / distance
            
            final_dx = dx + perpendicular_dx * zigzag_offset
            final_dy = dy + perpendicular_dy * zigzag_offset
            
            final_distance = math.sqrt(final_dx**2 + final_dy**2)
            if final_distance > 0:
                self.movement_direction = (final_dx/final_distance, final_dy/final_distance)

    def _charge_attack(self, player_pos: tuple[int, int]) -> None:
        """
Реализует паттерн атаки рывком на игрока.
"""
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.movement_direction = (dx/distance, dy/distance)
            self.speed = self.charge_speed
        else:
            self.speed = self.difficulty.value["enemy_speed"]

    def _tactical_attack(self, player_pos: tuple[int, int]) -> None:
        """
Реализует тактический паттерн атаки с укрытиями.
"""
        if not self.current_path or self.path_index >= len(self.current_path):
            cover_pos = self._find_nearest_cover(player_pos)
            if cover_pos:
                self.current_path = self.pathfinder.find_path((self.rect.centerx, self.rect.centery), cover_pos)
                self.path_index = 0
            else:
                self._set_new_patrol_point()
        
        if self.current_path:
            target_pos = self.current_path[self.path_index]
            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.speed:
                self.movement_direction = (dx/distance, dy/distance)
            else:
                self.path_index += 1
                if self.path_index >= len(self.current_path):
                    self.current_path = []

    def _find_nearest_cover(self, player_pos: tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
Находит ближайшее укрытие для врага.
"""
        cover_points = [
            (50, 50), (Config.SCREEN_WIDTH - 50, 50),
            (50, Config.SCREEN_HEIGHT - 50), (Config.SCREEN_WIDTH - 50, Config.SCREEN_HEIGHT - 50)
        ]
        best_cover = None
        min_dist = float('inf')
        for i in range(len(cover_points)):
            point = cover_points[i]
            dist = math.sqrt((self.rect.centerx - point[0])**2 + (self.rect.centery - point[1])**2)
            if dist < min_dist:
                best_cover = point
                min_dist = dist
        return best_cover

    def draw(self, screen: pygame.Surface) -> None:
        """
Рисует врага и его полоску здоровья.
"""
        screen.blit(self.image, self.rect)
        
        health_bar_width = self.rect.width * (self.health / self.max_health)
        health_bar_height = 5
        
        pygame.draw.rect(
            screen,
            Config.GREEN,
            (self.rect.x, self.rect.y - health_bar_height - 5, health_bar_width, health_bar_height)
        )
        
        if self.max_health > 1:
            pygame.draw.rect(
                screen,
                Config.RED,
                (self.rect.x + health_bar_width, self.rect.y - health_bar_height - 5, self.rect.width - health_bar_width, health_bar_height)
            )

class Boss(Enemy):
    BOSS_HEALTH = 100
    BOSS_SPEED = 2
    
    def __init__(self, difficulty: Difficulty):
        super().__init__(difficulty, level=4)
        
        self.health = self.BOSS_HEALTH * difficulty.value["boss_health_multiplier"]
        self.max_health = self.health
        self.speed = self.BOSS_SPEED * difficulty.value["boss_speed_multiplier"]
        
        self.rect.centerx = Config.SCREEN_WIDTH // 2
        self.rect.top = 50
        
        self.attack_cooldown = 2000
        self.last_attack_time = 0

    def update(self, player_pos: tuple[int, int] = None) -> None:
        super().update(player_pos)
        
        current_time = pygame.time.get_ticks()
        if self.should_attack(current_time):
            self.attack()
            self.last_attack_time = current_time

    def should_attack(self) -> bool:
        return pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown
