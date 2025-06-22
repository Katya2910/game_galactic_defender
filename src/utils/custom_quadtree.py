from typing import List, Tuple, Optional
import pygame

class CustomQuadTree:
    def __init__(self, x: float, y: float, width: float, height: float, max_objects: int = 4):
        self.bounds = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        self.max_objects = max_objects
        self.objects: List[pygame.sprite.Sprite] = []
        self.nodes: List[Optional['CustomQuadTree']] = [None] * 4
        self.divided = False

    def clear(self) -> None:
        """Очищает все объекты из квадранта"""
        self.objects.clear()
        self.divided = False
        for i in range(4):
            if self.nodes[i]:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self) -> None:
        """Разделяет квадрант на четыре подквадранта"""
        sub_width = self.bounds['width'] / 2
        sub_height = self.bounds['height'] / 2
        x = self.bounds['x']
        y = self.bounds['y']

        # Создаём четыре подквадранта
        self.nodes[0] = CustomQuadTree(x + sub_width, y, sub_width, sub_height, self.max_objects)  # Северо-восток
        self.nodes[1] = CustomQuadTree(x, y, sub_width, sub_height, self.max_objects)  # Северо-запад
        self.nodes[2] = CustomQuadTree(x, y + sub_height, sub_width, sub_height, self.max_objects)  # Юго-запад
        self.nodes[3] = CustomQuadTree(x + sub_width, y + sub_height, sub_width, sub_height, self.max_objects)  # Юго-восток

        self.divided = True

    def get_index(self, rect):
        indices = []
        vertical_midpoint = self.bounds['x'] + (self.bounds['width'] / 2)
        horizontal_midpoint = self.bounds['y'] + (self.bounds['height'] / 2)
        top_quadrant = rect.top < horizontal_midpoint
        bottom_quadrant = rect.bottom > horizontal_midpoint
        if rect.left < vertical_midpoint < rect.right:
            if top_quadrant:
                indices.append(1)
            if bottom_quadrant:
                indices.append(2)
        if rect.right > vertical_midpoint > rect.left:
            if top_quadrant:
                indices.append(0)
            if bottom_quadrant:
                indices.append(3)
        return indices

    def insert(self, obj):
        if not self._intersects(obj.rect):
            return False
        if len(self.objects) < self.max_objects and not self.divided:
            self.objects.append(obj)
            return True
        if not self.divided:
            self.split()
        if self.divided:
            for existing_obj in self.objects[:]:
                indices = self.get_index(existing_obj.rect)
                for index in indices:
                    self.nodes[index].insert(existing_obj)
            self.objects.clear()
        indices = self.get_index(obj.rect)
        for index in indices:
            self.nodes[index].insert(obj)
        return True

    def _intersects(self, rect):
        return not (rect.right < self.bounds['x'] or
                   rect.left > self.bounds['x'] + self.bounds['width'] or
                   rect.bottom < self.bounds['y'] or
                   rect.top > self.bounds['y'] + self.bounds['height'])

    def query(self, rect, found = None):
        if found is None:
            found = []
        if not self._intersects(rect):
            return found
        for obj in self.objects:
            if rect.colliderect(obj.rect):
                found.append(obj)
        if self.divided:
            for node in self.nodes:
                if node:
                    node.query(rect, found)
        return found

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.bounds['x'], self.bounds['y'], 
                         self.bounds['width'], self.bounds['height']), 1)
        if self.divided:
            for node in self.nodes:
                if node:
                    node.draw(screen) 