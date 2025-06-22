from .game_settings import GameSettings
from .colors import Colors
from .player_config import PlayerConfig
from .bullet_config import BulletConfig
from .enemy_config import EnemyConfig
from .boss_config import BossConfig, FinalBossConfig, MiniSpawnerBossConfig
from .platform_config import PlatformConfig
from .combat_config import CombatConfig
from .ui_config import UIConfig
from .movement_config import MovementConfig
from .paths_config import PathsConfig
"""
    # Главный класс для доступа ко всем настройкам игры.
"""
class Config:
    Game = GameSettings()
    ColorsInstance = Colors()
    Player = PlayerConfig()
    Bullet = BulletConfig()
    Enemy = EnemyConfig()
    Boss = BossConfig()
    FinalBoss = FinalBossConfig()
    MiniSpawnerBoss = MiniSpawnerBossConfig()
    Platform = PlatformConfig()
    Combat = CombatConfig()
    UI = UIConfig()
    Movement = MovementConfig()
    Paths = PathsConfig()

    # Основные параметры экрана
    SCREEN_WIDTH = GameSettings().SCREEN_WIDTH
    SCREEN_HEIGHT = GameSettings().SCREEN_HEIGHT
    FPS = GameSettings().FPS
    BG_COLOR = GameSettings().BG_COLOR
    
    # Цвета
    WHITE = Colors().WHITE
    RED = Colors().RED
    GREEN = Colors().GREEN
    BLUE = Colors().BLUE
    YELLOW = Colors().YELLOW
    PURPLE = Colors().PURPLE
    
    # Параметры игрока и объектов
    PLAYER_SPEED = PlayerConfig().SPEED
    BULLET_SPEED = BulletConfig().SPEED
    FONT_SIZE = UIConfig().FONT_SIZE
    
    # Пути к ресурсам
    ASSETS_DIR = PathsConfig().ASSETS_DIR
    IMAGES_DIR = PathsConfig().IMAGES_DIR
    SAVE_FILE = PathsConfig().SAVE_FILE
    MAIN_BACKGROUND = PathsConfig().MAIN_BACKGROUND
    ENEMY_LEVEL1_IMAGE = PathsConfig().ENEMY_LEVEL1_IMAGE

    LEVEL1_BACKGROUND = PathsConfig().LEVEL1_BACKGROUND
    LEVEL2_BACKGROUND = PathsConfig().LEVEL2_BACKGROUND
    LEVEL3_BACKGROUND = PathsConfig().LEVEL3_BACKGROUND
    LEVEL4_BACKGROUND = PathsConfig().LEVEL4_BACKGROUND
    TRANSITION_BACKGROUND = PathsConfig().TRANSITION_BACKGROUND

    ENEMY_LEVEL1_IMAGE = PathsConfig().ENEMY_LEVEL1_IMAGE
    ENEMY_LEVEL2_IMAGE = PathsConfig().ENEMY_LEVEL2_IMAGE
    ENEMY_LEVEL3_BOSS_IMAGE = PathsConfig().ENEMY_LEVEL3_BOSS_IMAGE
    MAIN_HERO_IMAGE = PathsConfig().MAIN_HERO_IMAGE

    PLATFORM_LEVEL2_IMAGE = PathsConfig().PLATFORM_LEVEL2_IMAGE
    PLATFORM_LEVEL3_IMAGE = PathsConfig().PLATFORM_LEVEL3_IMAGE
    
    @classmethod
    def init_assets(cls) -> None:
        """Инициализация директорий и ресурсов (создание папок, если нужно)."""
        cls.Paths.init_assets()

config = Config()

__all__ = ['Config', 'config']