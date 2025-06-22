from dataclasses import dataclass

"""
    # Параметры интерфейса пользователя (UI).
"""
@dataclass
class UIConfig:
    FONT_SIZE: int = 32              # Размер основного шрифта
    FONT_SIZE_SMALL: int = 20        # Маленький шрифт
    FONT_SIZE_TINY: int = 24         # Очень маленький шрифт
    HEALTH_BAR_HEIGHT: int = 5       # Высота полосы здоровья
    HEALTH_BAR_OFFSET: int = 10      # Отступ полосы здоровья
    BUTTON_WIDTH: int = 300          # Ширина кнопки
    BUTTON_HEIGHT: int = 70          # Высота кнопки
    BUTTON_BORDER_RADIUS: int = 15   # Радиус скругления кнопки 