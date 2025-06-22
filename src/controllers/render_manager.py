import pygame
from src.config import Config
from src.utils.enums import GameState
"""
    # Управляет отрисовкой игровых и неигровых экранов
"""
class RenderManager:
    def __init__(self, controller):
        self.controller = controller

    def refresh_menu(self):
        pass

    def refresh_story(self):
        pass

    def project_scene(self):
        # Основной метод отрисовки текущего состояния игры
        controller = self.controller
        controller.screen.fill(Config.BG_COLOR)
        if controller.game_state == GameState.GAME:
            controller.quadtree.draw(controller.screen)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - controller.timer_start) / 1000
            remaining_time = max(0, controller.game_timer - elapsed_time)
            controller.game_view.render(
                controller.player,
                controller.enemies,
                controller.boss,
                controller.score_manager.get_score(),
                remaining_time,
                controller.enemies_killed,
                controller.required_kills,
                controller.platforms,
                controller.level
            )
            controller.object_manager.advance_simulation()
        elif controller.game_state == GameState.MENU:
            controller.menu_view.render()
        elif controller.game_state == GameState.STORY:
            controller.story_view.render(controller.story_manager.get_current_story())
        elif controller.game_state == GameState.GAME_OVER:
            controller.game_view.draw_game_over()
        elif controller.game_state == GameState.VICTORY:
            controller.game_view.draw_victory_screen()
        pygame.display.flip()

    def render(self):
        self.project_scene()
        self.refresh_menu()
        self.refresh_story()
