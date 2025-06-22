import os
from dataclasses import dataclass

"""
    # Пути к основным ресурсам игры.
"""
@dataclass
class PathsConfig:
    ASSETS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")  # Папка с ассетами
    IMAGES_DIR: str = os.path.join(ASSETS_DIR, "images")                                 # Папка с изображениями
    SAVE_FILE: str = os.path.join(ASSETS_DIR, "save.json")                              # Файл сохранения
    MAIN_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "main_background.jpg")
    LEVEL1_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "background_level1.jpg")
    LEVEL2_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "background_level2.jpg")
    LEVEL3_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "background_level3.jpg")
    LEVEL4_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "background_level4.jpg")
    TRANSITION_BACKGROUND: str = os.path.join(IMAGES_DIR, "backgrounds", "background_transition_between_levels.jpg")
    ENEMY_LEVEL1_IMAGE: str = os.path.join(IMAGES_DIR, "enemies", "enemy_level_1.png")
    ENEMY_LEVEL2_IMAGE: str = os.path.join(IMAGES_DIR, "enemies", "enemy_level_2.png")
    ENEMY_LEVEL3_BOSS_IMAGE: str = os.path.join(IMAGES_DIR, "enemies", "enemy_level_3_boss.png")
    MAIN_HERO_IMAGE: str = os.path.join(IMAGES_DIR, "main_hero.png")
    PLATFORM_LEVEL2_IMAGE: str = os.path.join(IMAGES_DIR, "platforms", "platform_level_2.png")
    PLATFORM_LEVEL3_IMAGE: str = os.path.join(IMAGES_DIR, "platforms", "platform_level_3.png")
    
    @classmethod
    def init_assets(cls) -> None:
        """Создаёт необходимые папки для ассетов, если их нет."""
        os.makedirs(cls.IMAGES_DIR, exist_ok=True)