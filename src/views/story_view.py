import pygame
from src.config.config import Config
"""
    # Отвечает за визуализацию сюжетных вставок и обработку кликов
"""

class StoryView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, Config.FONT_SIZE)
        self.title_font = pygame.font.Font(None, Config.FONT_SIZE * 2)
        self.continue_button = pygame.Rect(
            Config.SCREEN_WIDTH // 2 - 100,
            Config.SCREEN_HEIGHT - 100,
            200,
            50
        )
        try:
            self.transition_bg = pygame.image.load("src/assets/images/backgrounds/background_transition_between_levels.jpg")
            self.transition_bg = pygame.transform.scale(self.transition_bg, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        except pygame.error:
            self.transition_bg = None

    def render(self, story_text: str) -> None:
        # Рендер сюжетной вставки с текстом и кнопкой продолжения
        if self.transition_bg:
            self.screen.blit(self.transition_bg, (0, 0))
        else:
            self.screen.fill(Config.BG_COLOR)
        enemy_img = pygame.image.load("src/assets/images/main_hero.png")
        img_size = 220
        enemy_img = pygame.transform.scale(enemy_img, (img_size, img_size))
        img_x = 80
        img_y = Config.SCREEN_HEIGHT // 2 - img_size // 2
        self.screen.blit(enemy_img, (img_x, img_y))

        arrow_start = (img_x + img_size, img_y + img_size // 2)
        arrow_end = (img_x + img_size + 80, img_y + img_size // 2)
        pygame.draw.line(self.screen, Config.WHITE, arrow_start, arrow_end, 6)
        pygame.draw.polygon(self.screen, Config.WHITE, [
            (arrow_end[0], arrow_end[1]),
            (arrow_end[0] - 20, arrow_end[1] - 15),
            (arrow_end[0] - 20, arrow_end[1] + 15)
        ])

        block_x = arrow_end[0] + 30
        block_y = img_y
        block_w = Config.SCREEN_WIDTH - block_x - 60
        block_h = img_size
        block_rect = pygame.Rect(block_x, block_y, block_w, block_h)
        pygame.draw.rect(self.screen, (30, 30, 60), block_rect, border_radius=18)
        pygame.draw.rect(self.screen, Config.WHITE, block_rect, 3, border_radius=18)

        if story_text:
            words = story_text.split()
            lines = []
            current_line = []
            font = self.font
            max_width = block_w - 40
            for word in words:
                test_line = ' '.join(current_line + [word])
                text_surface = font.render(test_line, True, Config.WHITE)
                if text_surface.get_width() < max_width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            y = block_y + 30
            for line in lines:
                text = font.render(line, True, Config.WHITE)
                text_rect = text.get_rect(x=block_x + 20, y=y)
                self.screen.blit(text, text_rect)
                y += font.get_height() + 10

        pygame.draw.rect(self.screen, Config.BLUE, self.continue_button, border_radius=12)
        continue_text = self.font.render("Продолжить", True, Config.WHITE)
        text_rect = continue_text.get_rect(center=self.continue_button.center)
        self.screen.blit(continue_text, text_rect)

    def handle_click(self, pos: tuple[int, int]) -> bool:
        # Обработка клика по кнопке 'Продолжить'
        if self.continue_button.collidepoint(pos):
            return True
        return False

    def update(self) -> None:
        pass  # Пока анимаций нет