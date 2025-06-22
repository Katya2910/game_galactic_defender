from typing import List, Tuple
import pygame
"""
    # Модуль для пространственного разбиения (QuadTree) для ускорения поиска коллизий
"""
class QuadTree:
    # Пространственное дерево для ускоренного поиска объектов в 2D
    def __init__(self, boundary: Tuple[float, float, float, float], capacity: int):
        # boundary: (x, y, width, height) — границы области
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def clear(self) -> None:
        self.objects = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        # Делит область на 4 поддерева
        x, y, w, h = self.boundary
        nw = (x, y, w / 2, h / 2)
        ne = (x + w / 2, y, w / 2, h / 2)
        sw = (x, y + h / 2, w / 2, h / 2)
        se = (x + w / 2, y + h / 2, w / 2, h / 2)

        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def insert(self, obj: pygame.sprite.Sprite) -> bool:
        # Пытается добавить объект в дерево. Возвращает True при успехе
        if not self._intersects(obj.rect):
            return False

        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True

        if not self.divided:
            self.subdivide()

        return (self.northwest.insert(obj) or
                self.northeast.insert(obj) or
                self.southwest.insert(obj) or
                self.southeast.insert(obj))

    def _intersects(self, rect: pygame.Rect) -> bool:
        # Проверяет, пересекается ли прямоугольник с областью дерева
        x, y, w, h = self.boundary
        return not (rect.right < x or
                   rect.left > x + w or
                   rect.bottom < y or
                   rect.top > y + h)

    def query(self, rect, found = None):
        if found is None:
            found = []
        if not self._intersects(rect):
            return found
        for obj in self.objects:
            if rect.colliderect(obj.rect):
                found.append(obj)
        if self.divided:
            self.northwest.query(rect, found)
            self.northeast.query(rect, found)
            self.southwest.query(rect, found)
            self.southeast.query(rect, found)
        return found

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует границы дерева на экране (для отладки)."""
        x, y, w, h = self.boundary
        pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h), 1)
        
        if self.divided:
            self.northwest.draw(screen)
            self.northeast.draw(screen)
            self.southwest.draw(screen)
            self.southeast.draw(screen) 