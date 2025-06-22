from typing import Union
import pygame
from src.models.entity import Entity
from src.models.bullet import Bullet
from src.config.config import Config
"""
    # Игрок: движение, стрельба
"""
class Player(Entity):
    def __init__(self, bullet_sound=None):
        super().__init__(
            Config.SCREEN_WIDTH // 2 - 25,
            Config.SCREEN_HEIGHT - 50,
            50, 40, Config.BLUE
        )
        hero_img = pygame.image.load("src/assets/images/main_hero.png")
        hero_img = pygame.transform.scale(hero_img, (int(75 * 1.5), int(60 * 1.5)))
        self.image = hero_img
        self.rect = self.image.get_rect()
        self.rect.x = Config.SCREEN_WIDTH // 2 - int(75 * 1.5) // 2
        self.rect.y = Config.SCREEN_HEIGHT - int(60 * 1.5)
        self.speed = Config.PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.bullet_sound = bullet_sound

    def update(self) -> None:
        self._handle_movement()
        self.bullets.update()

    def _handle_movement(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < Config.SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < Config.SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(
                self.rect.centerx, 
                self.rect.top
            )
            self.bullets.add(bullet)
            if self.bullet_sound:
                self.bullet_sound.play()
            return bullet
        return None

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface, always_show_health_bar=True) 