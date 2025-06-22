import pygame
from src.models.entity import Entity
from src.config.config import Config
"""
    # Платформа для уровней 2 и 3
"""
class Platform(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, level: int = 1):
        # width = int(width * 2)
        # height = int(height * 2)
        super().__init__(x, y, width, height, Config.YELLOW if level == 3 else Config.WHITE)
        self.rect = pygame.Rect(x, y, width, height)
        self.level = level
        if level == 3:
            img = pygame.image.load("src/assets/images/platforms/platform_level_3.png")
            img = pygame.transform.scale(img, (width, height))
            self.image = img
        elif level == 2:
            img = pygame.image.load("src/assets/images/platforms/platform_level_2.png")
            img = pygame.transform.scale(img, (width, height))
            self.image = img
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(Config.WHITE)
        
    def update(self) -> None:
        """Платформа статична, обновление не требуется."""
        pass
        
    @staticmethod
    def create_platforms(level: int) -> list:
        """Создаёт список платформ для заданного уровня."""
        platforms = []
        
        if level == 2:
            platform_sizes = [
                (150, 20),
                (150, 20),  
            ]
            
            positions = [
                (300, 200),   
                (500, 400),   
            ]
            
            for i in range(len(positions)):
                pos = positions[i]
                size = platform_sizes[i]
                platforms.append(Platform(pos[0], pos[1], size[0], size[1], level))
                
        elif level == 3:
            platform_sizes = [
                (300, 30),   
                (300, 30),  
                (200, 30),  
                (200, 30),  
                (150, 30),   
            ]
            
            positions = [
                (100, 100),    
                (100, 590),  
                (50, 200),     
                (1030, 200),   
                (565, 345),     
            ]
            
            for i in range(len(positions)):
                pos = positions[i]
                size = platform_sizes[i]
                platforms.append(Platform(pos[0], pos[1], size[0], size[1], level))
            
        return platforms 