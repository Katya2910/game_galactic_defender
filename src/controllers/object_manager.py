import pygame
from src.models.enemy import Enemy
from src.models.platform import Platform
from src.utils.enums import GameState
"""
    # Класс для управления врагами, платформами и обработкой коллизий.
"""
class ObjectManager:
    def __init__(self, controller):
        self.controller = controller

    def deploy_invaders(self):
        """
Создаёт врагов для текущего уровня.
"""
        controller = self.controller
        controller.enemies.empty()
        if controller.level == 2:
            num_enemies = 5
        else:
            num_enemies = 5 + (controller.level * 2)
        i = 0
        while i < num_enemies:
            if controller.level == 2:
                if i % 2 == 0:
                    enemy_level = 2
                else:
                    enemy_level = 1
            elif controller.level == 3:
                enemy_level = 1
            else:
                enemy_level = 1
            enemy = Enemy(controller.difficulty, level=enemy_level)
            controller.enemies.add(enemy)
            controller.all_sprites.add(enemy)
            i += 1

    def deploy_platforms(self):
        """
Создаёт платформы для текущего уровня (если нужны).
"""
        controller = self.controller
        if controller.level == 2 or controller.level == 3:
            controller.platforms.empty()
            platforms = Platform.create_platforms(controller.level)
            for platform in platforms:
                controller.platforms.add(platform)
                controller.all_sprites.add(platform)

    def resolve_impacts(self):
        """
Проверяет и обрабатывает все коллизии между объектами игры.
"""
        controller = self.controller
        controller.quadtree.clear()
        for enemy in controller.enemies:
            if enemy.level == 3:
                controller.quadtree.max_objects = 4
            else:
                controller.quadtree.max_objects = 8
            controller.quadtree.insert(enemy)
        if controller.boss:
            controller.quadtree.insert(controller.boss)
            for mini_enemy in getattr(controller.boss, 'mini_enemies', []):
                controller.quadtree.insert(mini_enemy)
        for platform in controller.platforms:
            controller.quadtree.insert(platform)
        for bullet in controller.player.bullets:
            potential_collisions = controller.quadtree.query(bullet.rect)
            for obj in potential_collisions:
                if pygame.sprite.collide_rect(bullet, obj):
                    if isinstance(obj, Platform):
                        bullet.kill()
                        continue
                    obj.health -= bullet.damage
                    bullet.kill()
                    if obj.health <= 0:
                        if hasattr(obj, 'level') and obj.level == 2 and controller.level == 2:
                            controller.score_manager.add_score(20)
                        else:
                            controller.score_manager.add_score(obj.score_value)
                        if not hasattr(obj, 'is_mini_enemy'):
                            controller.enemies_killed += 1
                        obj.kill()
        for enemy in controller.enemies:
            potential_collisions = controller.quadtree.query(enemy.rect)
            for obj in potential_collisions:
                if isinstance(obj, Platform) and pygame.sprite.collide_rect(enemy, obj):
                    if enemy.rect.bottom > obj.rect.top > enemy.rect.top:
                        enemy.rect.bottom = obj.rect.top
                    elif enemy.rect.top < obj.rect.bottom < enemy.rect.bottom:
                        enemy.rect.top = obj.rect.bottom
                    if enemy.rect.right > obj.rect.left > enemy.rect.left:
                        enemy.rect.right = obj.rect.left
                    elif enemy.rect.left < obj.rect.right < enemy.rect.right:
                        enemy.rect.left = obj.rect.right
        for platform in controller.platforms:
            if pygame.sprite.collide_rect(controller.player, platform):
                if controller.player.rect.bottom > platform.rect.top > controller.player.rect.top:
                    controller.player.rect.bottom = platform.rect.top
                elif controller.player.rect.top < platform.rect.bottom < controller.player.rect.bottom:
                    controller.player.rect.top = platform.rect.bottom
                if controller.player.rect.right > platform.rect.left > controller.player.rect.left:
                    controller.player.rect.right = platform.rect.left
                elif controller.player.rect.left < platform.rect.right < controller.player.rect.right:
                    controller.player.rect.left = platform.rect.right
        for enemy in controller.enemies:
            if pygame.sprite.collide_rect(controller.player, enemy):
                controller.player.health -= 10
                enemy.health -= 20
                if enemy.health <= 0:
                    if enemy.level == 2 and controller.level == 2:
                        controller.score_manager.add_score(20)
                    else:
                        controller.score_manager.add_score(enemy.score_value)
                    controller.enemies_killed += 1
                    enemy.kill()
        if controller.boss:
            for mini_enemy in getattr(controller.boss, 'mini_enemies', []):
                if pygame.sprite.collide_rect(controller.player, mini_enemy):
                    controller.player.health -= 10
                    mini_enemy.health -= 20
                    if mini_enemy.health <= 0:
                        mini_enemy.kill()
            if controller.boss and pygame.sprite.collide_rect(controller.player, controller.boss):
                controller.player.health -= 20
                if controller.player.health <= 0:
                    controller.boss.kill()
        if len(controller.enemies) == 0 and not controller.level_completed:
            if (controller.level == 1 or controller.level == 2 or controller.level == 3) and controller.enemies_killed < controller.required_kills:
                self.deploy_invaders()
            else:
                controller.level_completed = True
                controller.level_manager.level_complete()

    def advance_simulation(self):
        """
Обновляет состояние всех игровых объектов и проверяет условия завершения уровня.
"""
        controller = self.controller
        controller.player.update()
        if controller.player.health <= 0:
            controller.game_state = GameState.GAME_OVER
            return
        controller.all_sprites.update()
        controller.platforms.update()
        player_pos = (controller.player.rect.x, controller.player.rect.y)
        for enemy in controller.enemies:
            enemy.update(player_pos)
        if controller.boss:
            controller.boss.update(player_pos)
            if controller.boss.health <= 0:
                controller.boss.kill()
                controller.boss = None
                if controller.level == 4:
                    controller.level_manager.level_complete()
                if controller.level == 3:
                    controller.game_state = GameState.VICTORY
        self.resolve_impacts()
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - controller.timer_start) / 1000
        remaining_time = max(0, controller.game_timer - elapsed_time)
        if controller.level == 4:
            if remaining_time <= 0:
                if controller.boss is not None and controller.boss.health > 0:
                    controller.game_state = GameState.GAME_OVER
                    return
        else:
            if remaining_time <= 0:
                if controller.enemies_killed < controller.required_kills:
                    controller.game_state = GameState.GAME_OVER
                    return
                else:
                    controller.level_manager.level_complete()
                    return
            elif controller.enemies_killed >= controller.required_kills:
                controller.level_manager.level_complete()
                return 