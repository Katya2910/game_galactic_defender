import pygame
from typing import List, Optional
from src.models.player import Player
from src.models.enemy import Enemy, Boss
from src.config.config import Config
from src.utils.score_manager import ScoreManager
"""
    # Отвечает за визуализацию игрового процесса и экранов состояния
"""
class GameView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.score_manager = ScoreManager()

        self.main_background = pygame.image.load(Config.MAIN_BACKGROUND)
        self.main_background = pygame.transform.scale(self.main_background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.level1_background = pygame.image.load(Config.LEVEL1_BACKGROUND)
        self.level1_background = pygame.transform.scale(self.level1_background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.level2_background = pygame.image.load(Config.LEVEL2_BACKGROUND)
        self.level2_background = pygame.transform.scale(self.level2_background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.level3_background = pygame.image.load(Config.LEVEL3_BACKGROUND)
        self.level3_background = pygame.transform.scale(self.level3_background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.level4_background = pygame.image.load(Config.LEVEL4_BACKGROUND)
        self.level4_background = pygame.transform.scale(self.level4_background, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.transition_bg = pygame.image.load("src/assets/images/backgrounds/background_transition_between_levels.jpg")
        self.transition_bg = pygame.transform.scale(self.transition_bg, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

    def render(
        self,
        player: Player,
        enemies: pygame.sprite.Group,
        boss: Optional[Boss],
        score: int,
        remaining_time: float = 0,
        enemies_killed: int = 0,
        required_kills: int = 10,
        platforms: Optional[pygame.sprite.Group] = None,
        level: int = 1
    ) -> None:
        # Основной игровой рендер: фон, игрок, враги, платформы, HUD
        if level == 4 and self.level4_background:
            self.screen.blit(self.level4_background, (0, 0))
        elif level == 3 and self.level3_background:
            self.screen.blit(self.level3_background, (0, 0))
        elif level == 2 and self.level2_background:
            self.screen.blit(self.level2_background, (0, 0))
        elif level == 1 and self.level1_background:
            self.screen.blit(self.level1_background, (0, 0))
        elif self.main_background:
            self.screen.blit(self.main_background, (0, 0))
        else:
            self.screen.fill(Config.BG_COLOR)

        player.draw(self.screen)
        for enemy in enemies:
            enemy.draw(self.screen)
        if boss:
            boss.draw(self.screen)
        player.bullets.draw(self.screen)
        
        if platforms:
            platforms.draw(self.screen)

        self._draw_hud(player.health, score, remaining_time, enemies_killed, required_kills)

    def _draw_hud(self, health: int, score: int, remaining_time: float, enemies_killed: int, required_kills: int) -> None:
        # HUD: здоровье, очки, таймер, количество убийств
        health_text = self.font.render(f"Health: {health}", True, Config.WHITE)
        self.screen.blit(health_text, (10, 10))

        score_text = self.font.render(f"Score: {score}", True, Config.WHITE)
        self.screen.blit(score_text, (Config.SCREEN_WIDTH - 150, 10))

        timer_text = self.font.render(f"Time: {remaining_time:.1f}s", True, Config.WHITE)
        self.screen.blit(timer_text, (Config.SCREEN_WIDTH // 2 - 50, 10))

        kills_text = self.font.render(f"Kills: {enemies_killed}/{required_kills}", True, Config.WHITE)
        self.screen.blit(kills_text, (Config.SCREEN_WIDTH // 2 - 50, 50))

    def draw_victory_screen(self) -> None:
        # Экран победы (вызывается при завершении игры)
        if self.transition_bg:
            self.screen.blit(self.transition_bg, (0, 0))
        else:
            self.screen.fill(Config.BG_COLOR)
        victory_text = self.font.render("ПОБЕДА!", True, Config.GREEN)
        text_rect = victory_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, text_rect)

        instruction = self.font.render("Нажмите ENTER, чтобы вернуться в меню", True, Config.WHITE)
        self.screen.blit(instruction, (Config.SCREEN_WIDTH // 2 - instruction.get_width() // 2, Config.SCREEN_HEIGHT // 2 + 100))

        score_text = self.font.render(
            f"Финальный счет: {self.score_manager.get_score()}",
            True,
            Config.WHITE
        )
        score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font.render(
            f"Рекорд: {self.score_manager.get_high_score()}",
            True,
            Config.WHITE
        )
        high_score_rect = high_score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(high_score_text, high_score_rect)

    def draw_game_over(self) -> None:
        # Экран поражения (вызывается при проигрыше)
        if self.transition_bg:
            self.screen.blit(self.transition_bg, (0, 0))
        else:
            self.screen.fill(Config.BG_COLOR)
        game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, Config.RED)
        text_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)

        instruction = self.font.render("Нажмите ENTER, чтобы вернуться в меню", True, Config.WHITE)
        self.screen.blit(instruction, (Config.SCREEN_WIDTH // 2 - instruction.get_width() // 2, Config.SCREEN_HEIGHT // 2 + 100))

        score_text = self.font.render(
            f"Финальный счет: {self.score_manager.get_score()}",
            True,
            Config.WHITE
        )
        score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font.render(
            f"Рекорд: {self.score_manager.get_high_score()}",
            True,
            Config.WHITE
        )
        high_score_rect = high_score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(high_score_text, high_score_rect)

    def draw_story(self, story_text: str) -> None:
        # Экран сюжетной вставки
        self.screen.fill(Config.BG_COLOR)
        
        if story_text:
            lines = story_text.split('\n')
            y_pos = 150
            for line in lines:
                text = self.font.render(line, True, Config.WHITE)
                self.screen.blit(text, (Config.SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
                y_pos += 40

            continue_text = self.font.render("Нажмите ПРОБЕЛ для продолжения", True, Config.YELLOW)
            self.screen.blit(continue_text, (Config.SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))