from dataclasses import dataclass

"""
    # Параметры платформ для разных уровней.
"""
@dataclass
class PlatformConfig:
    SCALE_MULTIPLIER: int = 2  # Множитель масштаба платформ
    
    LEVEL2_SIZES: list = None      # Размеры платформ для 2 уровня
    LEVEL2_POSITIONS: list = None  # Позиции платформ для 2 уровня
    
    LEVEL3_SIZES: list = None      # Размеры платформ для 3 уровня
    LEVEL3_POSITIONS: list = None  # Позиции платформ для 3 уровня
    
    def __post_init__(self):
        """Инициализация размеров и позиций платформ по умолчанию."""
        if self.LEVEL2_SIZES is None:
            self.LEVEL2_SIZES = [(150, 20), (150, 20)]
        
        if self.LEVEL2_POSITIONS is None:
            self.LEVEL2_POSITIONS = [(300, 200), (500, 400)]
        
        if self.LEVEL3_SIZES is None:
            self.LEVEL3_SIZES = [(300, 30), (300, 30), (200, 30), (200, 30), (150, 30)]
        
        if self.LEVEL3_POSITIONS is None:
            self.LEVEL3_POSITIONS = [(100, 100), (100, 590), (50, 200), (1030, 200), (565, 345)] 