from dataclasses import dataclass

"""
    # Класс с основными цветами в формате RGB.
"""
@dataclass
class Colors:
    WHITE: tuple = (255, 255, 255)  # Белый
    RED: tuple = (255, 0, 0)        # Красный
    GREEN: tuple = (0, 255, 0)      # Зеленый
    BLUE: tuple = (0, 100, 255)     # Синий
    YELLOW: tuple = (255, 255, 0)   # Желтый
    PURPLE: tuple = (255, 0, 255)   # Фиолетовый
    BLACK: tuple = (0, 0, 0)        # Черный
    GRAY: tuple = (128, 128, 128)   # Серый
    DARK_GRAY: tuple = (50, 50, 50) # Темно-серый
    LIGHT_BLUE: tuple = (100, 150, 255) # Светло-синий