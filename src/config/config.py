"""
Модуль конфигурации для обратной совместимости.
Использует новую модульную структуру конфигурации.
"""

from . import Config
# Также экспортируем отдельные классы для прямого доступа
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
