import pygame
from src.config.config import Config
from src.utils.enums import Difficulty
"""
    # Отвечает за визуализацию главного меню и экранов состояния
"""
class MenuView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, Config.FONT_SIZE)
        self.title_font = pygame.font.SysFont('impact', Config.FONT_SIZE * 2)
        self.buttons = []
        self._create_buttons()

        self.background = pygame.image.load(Config.MAIN_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    def _create_buttons(self) -> None:
        # Кнопки главного меню
        button_width = 300
        button_height = 70
        button_x = (Config.SCREEN_WIDTH - button_width) // 2
        button_y = (Config.SCREEN_HEIGHT - button_height) // 2
        self.buttons = [
            {
                "text": "Начать игру",
                "rect": pygame.Rect(button_x, button_y, button_width, button_height),
                "action": "start"
            }
        ]

    def update(self) -> None:
        pass

    def render(self) -> None:
        # Рендер главного меню
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(Config.BG_COLOR)

        title = self.title_font.render("Galactic Defender", True, Config.WHITE)
        title_rect = title.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=50)
        self.screen.blit(title, title_rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, Config.BLUE, button["rect"], border_radius=15)
            text = self.font.render(button["text"], True, Config.WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos: tuple[int, int]) -> str:
        # Обработка клика по кнопкам меню
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                return button["action"]
        return ""

    def draw_game_over(self, score: int, high_score: int) -> None:
        # Экран поражения с очками и рекордом
        self.screen.fill(Config.BG_COLOR)
        
        game_over = self.title_font.render("Game Over", True, Config.RED)
        game_over_rect = game_over.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=100)
        self.screen.blit(game_over, game_over_rect)

        score_text = self.font.render(f"Score: {score}", True, Config.WHITE)
        score_rect = score_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=200)
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font.render(f"High Score: {high_score}", True, Config.WHITE)
        high_score_rect = high_score_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=250)
        self.screen.blit(high_score_text, high_score_rect)

        restart_text = self.font.render("Press R to Restart", True, Config.WHITE)
        restart_rect = restart_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=350)
        self.screen.blit(restart_text, restart_rect)

    def draw_victory(self, score: int, high_score: int) -> None:
        # Экран победы с очками и рекордом
        self.screen.fill(Config.BG_COLOR)
        
        victory = self.title_font.render("Victory!", True, Config.GREEN)
        victory_rect = victory.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=100)
        self.screen.blit(victory, victory_rect)

        score_text = self.font.render(f"Final Score: {score}", True, Config.WHITE)
        score_rect = score_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=200)
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font.render(f"High Score: {high_score}", True, Config.WHITE)
        high_score_rect = high_score_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=250)
        self.screen.blit(high_score_text, high_score_rect)

        menu_text = self.font.render("Press ESC for Menu", True, Config.WHITE)
        menu_rect = menu_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=350)
        self.screen.blit(menu_text, menu_rect) 