from src.config.config import Config
"""
    # Основной игровой цикл
"""
def cycle_cosmos(game):
    while game.running:
        game.event_handler.process_signals()
        # Явная проверка состояния
        if game.game_state == 1 or game.game_state == 2 or game.game_state == 3:
            game.object_manager.advance_simulation()
        game.render_manager.project_scene()
        game.clock.tick(Config.FPS) 