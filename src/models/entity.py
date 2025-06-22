import pygame
from abc import ABC, abstractmethod
from src.config.config import Config
"""
    # Базовый класс для всех игровых сущностей
"""
class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 1
        self.max_health = 1

    def draw(self, surface: pygame.Surface, always_show_health_bar: bool = False) -> None:
        surface.blit(self.image, self.rect)
        self.draw_health(surface, always_show=always_show_health_bar)

    def draw_health(self, surface: pygame.Surface, always_show: bool = False) -> None:
        if always_show or self.health < self.max_health:
            health_width = self.rect.width * (self.health / self.max_health)
            pygame.draw.rect(surface, Config.RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(surface, Config.GREEN, (self.rect.x, self.rect.y - 10, health_width, 5))

    def update(self) -> None:
        pass

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0 