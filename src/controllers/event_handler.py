import pygame
from src.utils.enums import GameState, Difficulty

"""
    # Обрабатывает события пользователя (клавиатура, мышь)
"""
class EventHandler:
    def __init__(self, controller):
        self.controller = controller

    def process_signals(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.running = False
            elif event.type == pygame.KEYDOWN:
                self._process_key_signal(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._process_mouse_signal(event.pos)

    def _process_key_signal(self, key):
        controller = self.controller
        if key == pygame.K_ESCAPE:
            controller.running = False
        elif key == pygame.K_RETURN:
            if controller.game_state == GameState.MENU:
                controller.level_manager.new_game()
            elif controller.game_state == GameState.STORY:
                if not controller.story_manager.has_next_story():
                    controller.level_completed = False
                    controller.enemies_killed = 0
                    controller.game_state = GameState.GAME
                    if controller.level == 4:
                        controller.required_kills = 0
                        controller.enemies_killed = 0
                        controller.boss = controller.final_boss_class(controller.difficulty)
                        controller.all_sprites.add(controller.boss)
                        controller.enemies.empty()
                        controller.platforms.empty()
                    else:
                        controller.boss = None
                        controller.object_manager.deploy_invaders()
                        if controller.level == 2 or controller.level == 3:
                            controller.object_manager.deploy_platforms()
                    controller.timer_start = pygame.time.get_ticks()
                else:
                    controller.story_manager.next_story()
            elif controller.game_state == GameState.GAME_OVER:
                controller.game_state = GameState.MENU
            elif controller.game_state == GameState.VICTORY:
                controller.game_state = GameState.MENU
        elif key == pygame.K_SPACE:
            if controller.game_state == GameState.GAME:
                controller.player.shoot()
        elif key == pygame.K_n:
            if controller.game_state == GameState.GAME:
                if controller.level < controller.max_levels:
                    controller.level += 1
                    controller.enemies_killed = 0
                    if controller.level < controller.max_levels:
                        controller.required_kills = 10
                    else:
                        controller.required_kills = 0
                    controller.boss = None
                    controller.enemies.empty()
                    controller.platforms.empty()
                    if controller.level == controller.max_levels:
                        controller.boss = controller.final_boss_class(controller.difficulty)
                        controller.all_sprites.add(controller.boss)
                    else:
                        controller.object_manager.deploy_invaders()
                        if controller.level == 2 or controller.level == 3:
                            controller.object_manager.deploy_platforms()
                    controller.timer_start = pygame.time.get_ticks()
                    controller.game_state = GameState.GAME
        elif controller.game_state == GameState.MENU:
            if key == pygame.K_1:
                controller.difficulty = Difficulty.EASY
                controller.level_manager.new_game()
            elif key == pygame.K_2:
                controller.difficulty = Difficulty.NORMAL
                controller.level_manager.new_game()
            elif key == pygame.K_3:
                controller.difficulty = Difficulty.HARD
                controller.level_manager.new_game()

    def _process_mouse_signal(self, pos):
        controller = self.controller
        if controller.game_state == GameState.MENU:
            action = controller.menu_view.handle_click(pos)
            if action == "start":
                controller.level_manager.new_game()
            elif action == "quit":
                controller.running = False
        elif controller.game_state == GameState.STORY:
            if controller.story_view.handle_click(pos):
                if controller.story_manager.has_next_story():
                    controller.story_manager.next_story()
                else:
                    controller.level_completed = False
                    controller.enemies_killed = 0
                    controller.game_state = GameState.GAME
                    if controller.level == 1:
                        controller.required_kills = 10
                    elif controller.level == 2:
                        controller.required_kills = 10
                    elif controller.level == 3:
                        controller.required_kills = 10
                    elif controller.level == 4:
                        controller.required_kills = 0
                        controller.enemies_killed = 0
                        controller.boss = controller.final_boss_class(controller.difficulty)
                        controller.all_sprites.add(controller.boss)
                        controller.enemies.empty()
                        controller.platforms.empty()
                    if controller.level != 4:
                        controller.boss = None
                        controller.object_manager.deploy_invaders()
                        if controller.level == 2 or controller.level == 3:
                            controller.object_manager.deploy_platforms()
                    controller.timer_start = pygame.time.get_ticks()

        self.controller.object_manager.deploy_invaders()
        self.controller.object_manager.deploy_platforms()