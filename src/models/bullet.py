from src.models.entity import Entity
from src.config.config import BulletConfig
import pygame

"""
    # Класс пули, выпущенной игроком.
"""
class Bullet(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BulletConfig.WIDTH, BulletConfig.HEIGHT, BulletConfig.COLOR)
        self.speed = -BulletConfig.SPEED
        self.damage = BulletConfig.DAMAGE
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """Движение пули вверх."""
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
