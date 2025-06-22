import pygame
from typing import Optional
from src.config.config import Config
from src.models.player import Player
from src.models.boss import Boss
from src.utils.quadtree import QuadTree
from src.utils.save_system import SaveSystem
from src.views.game_view import GameView
from src.views.menu_view import MenuView
from src.views.story_view import StoryView
from src.utils.enums import GameState, Difficulty
from src.utils.score_manager import ScoreManager
from src.models.bosses.final_boss import FinalBoss
from src.models.platform import Platform
from src.story.game_story import GameStory
from .event_handler import EventHandler
from .level_manager import LevelManager
from .object_manager import ObjectManager
from .render_manager import RenderManager

"""
    # Главный контроллер игры: инициализация, запуск, управление состояниями
"""
class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Galactic Defender")
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load("src/assets/sounds/game_sound.mp3")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)
        self.bullet_sound = pygame.mixer.Sound("src/assets/sounds/sound_bullet.mp3")
        self.bullet_sound.set_volume(0.5)
        self.player = Player(bullet_sound=self.bullet_sound)
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.boss: Optional[Boss] = None
        self.difficulty = Difficulty.NORMAL
        self.story_manager = GameStory()
        self.score_manager = ScoreManager()
        self.game_view = GameView(self.screen)
        self.menu_view = MenuView(self.screen)
        self.story_view = StoryView(self.screen)
        self.running = True
        self.game_state = GameState.MENU
        self.quadtree = QuadTree((0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), 4)
        saved_data = SaveSystem.load_game()
        self.high_score = saved_data.get("high_score", 0)
        self.game_timer = 30
        self.timer_start = 0
        self.enemies_killed = 0
        self.required_kills = 10
        self.max_levels = 4
        self.platforms = pygame.sprite.Group()
        self.level_completed = False
        self.level = 1
        self.event_handler = EventHandler(self)
        self.level_manager = LevelManager(self)
        self.object_manager = ObjectManager(self)
        self.render_manager = RenderManager(self)
        self.final_boss_class = FinalBoss

    def run(self):
        # Менее оптимальный цикл, явные проверки
        while self.running:
            self.clock.tick(60)
            self.event_handler.process_signals()
            if self.game_state == GameState.GAME:
                self.object_manager.advance_simulation()
            else:
                if self.game_state == GameState.MENU:
                    self.render_manager.refresh_menu()
                if self.game_state == GameState.STORY:
                    self.render_manager.refresh_story()
            self.render_manager.project_scene() 

    def commence_mission(self):
        pass
