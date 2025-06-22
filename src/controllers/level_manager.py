import pygame
from src.utils.enums import GameState
from src.utils.save_system import SaveSystem
"""
    # Управляет переходами между уровнями, условиями победы и поражения
"""
class LevelManager:
    def __init__(self, controller):
        self.controller = controller

    def new_game(self):
        # Запуск новой игры, сброс прогресса и сюжета
        controller = self.controller
        controller.level = 1
        controller.enemies_killed = 0
        controller.required_kills = 10
        controller.level_completed = False
        controller.score_manager.reset_score()
        controller.player.health = controller.player.max_health
        controller.story_manager.reset_story()
        controller.story_manager.story_parts = [
            {"title": "Глава 1: Начало", "text": "В 2157 году человечество столкнулось с угрозой из глубин космоса. Кибернетическая раса, известная как 'Кибернетики', начала массированное вторжение в Солнечную систему. Их цель - захватить Землю и превратить людей в свои биологические батареи."},
            {"title": "Глава 1: Надежда", "text": "Вы - лучший пилот Земного Флота, и именно вам поручена важнейшая миссия: прорваться через оборону противника и уничтожить их командный центр. На вашем экспериментальном истребителе установлена новейшая система улучшений, которая будет развиваться по мере уничтожения врагов."}
        ]
        controller.game_state = GameState.STORY
        controller.timer_start = pygame.time.get_ticks()

    def level_complete(self):
        # Переход на следующий уровень или завершение игры при победе
        controller = self.controller
        if controller.level == 1:
            if controller.enemies_killed >= controller.required_kills:
                controller.level += 1
                controller.enemies_killed = 0
                controller.story_manager.reset_story()
                controller.story_manager.story_parts = [
                    {"title": "Глава 2: Космический лабиринт", "text": "После успешного прорыва первой линии обороны, вы входите в опасную зону астероидов. Здесь Кибернетики устроили засаду. Это место известно как 'Космический лабиринт' - здесь погибло множество пилотов, пытавшихся прорваться к командному центру врага."},
                    {"title": "Глава 2: Испытание", "text": "Вам предстоит проявить все свое мастерство пилота, используя астероиды как укрытие и одновременно избегая засад врага. Каждый поворот может скрывать новую опасность, а каждый астероид может стать как вашим спасением, так и вашей гибелью."}
                ]
                controller.game_state = GameState.STORY
                return
            else:
                controller.game_state = GameState.GAME_OVER
                return
        elif controller.level == 2:
            if controller.enemies_killed >= controller.required_kills:
                controller.level += 1
                controller.enemies_killed = 0
                controller.story_manager.reset_story()
                controller.story_manager.story_parts = [
                    {"title": "Глава 3: Командный центр", "text": "Вы приближаетесь к командному центру Кибернетиков. Их защита усиливается с каждой минутой, а корабли становятся все более мощными и опасными. Здесь сосредоточены их основные силы и самые продвинутые технологии."},
                    {"title": "Глава 3: Последний рубеж", "text": "Используйте все доступные улучшения вашего корабля и проявите тактическое мышление. Это последний рубеж перед главной целью - уничтожением командного центра. Каждая победа приближает вас к финальной битве, но и каждая ошибка может стоить вам жизни."}
                ]
                controller.game_state = GameState.STORY
                return
            else:
                controller.game_state = GameState.GAME_OVER
                return
        elif controller.level == 3:
            if controller.enemies_killed >= controller.required_kills:
                controller.level += 1
                controller.enemies_killed = 0
                controller.story_manager.reset_story()
                controller.story_manager.story_parts = [
                    {"title": "Глава 4: Финальная битва", "text": "Перед вами - главный командный центр Кибернетиков. Его защищает огромный флот и мощный босс - гигантский космический корабль, оснащенный самым передовым оружием. Это ваша последняя битва, от которой зависит судьба всего человечества."},
                    {"title": "Глава 4: Новое начало", "text": "С уничтожением командного центра, флот Кибернетиков потеряет координацию, и человечество получит шанс нанести ответный удар. Но это только начало новой главы в истории космических сражений, и кто знает, какие еще испытания ждут человечество в будущем..."}
                ]
                controller.game_state = GameState.STORY
                return
            else:
                controller.game_state = GameState.GAME_OVER
                return
        elif controller.level == 4:
            if controller.boss is None:
                controller.game_state = GameState.VICTORY
            return

    def game_over(self):
        # Обработка состояния поражения (GAME_OVER)
        controller = self.controller
        controller.game_state = GameState.GAME_OVER
        if controller.score_manager.score > controller.high_score:
            controller.high_score = controller.score_manager.score
            SaveSystem.save_game({"high_score": controller.high_score})

    def victory(self):
        # Обработка состояния победы (VICTORY)
        controller = self.controller
        controller.game_state = GameState.VICTORY
        if controller.score_manager.score > controller.high_score:
            controller.high_score = controller.score_manager.score
            SaveSystem.save_game({"high_score": controller.high_score})

    def check_victory_condition(self):
        # Проверяет условие победы на уровне
        controller = self.controller
        if not controller.enemies and not controller.boss:
            if controller.level >= 15:
                controller.game_state = GameState.VICTORY
                if controller.score_manager.get_score() > controller.score_manager.get_high_score():
                    SaveSystem.save_game({"high_score": controller.score_manager.get_score()})
            else:
                if controller.story_manager.has_next_story():
                    controller.game_state = GameState.STORY
                controller.deploy_invaders() 