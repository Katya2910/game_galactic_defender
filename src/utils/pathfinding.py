from typing import List, Tuple, Dict, Set
import heapq
import math
"""
    # Модуль для поиска пути (алгоритм Theta*) с учетом препятствий
"""
class Node:
    # Узел для алгоритма поиска пути Theta*
    def __init__(self, position: Tuple[int, int], g_cost: float = float('inf'), h_cost: float = float('inf')):
        self.position = position
        self.g_cost = g_cost  # Стоимость пути от старта до текущей точки
        self.h_cost = h_cost  # Оценочная стоимость от текущей точки до цели
        self.f_cost = g_cost + h_cost  # Общая стоимость
        self.parent = None

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class ThetaStar:
    # Поиск пути по алгоритму Theta* (any-angle pathfinding)
    def __init__(self, grid_size: Tuple[int, int], obstacle_positions: List[Tuple[int, int]] = None):
        self.grid_size = grid_size
        self.obstacles = set(obstacle_positions) if obstacle_positions else set()
        self.directions = [
            (0, 1),   # вправо
            (1, 0),   # вниз
            (0, -1),  # влево
            (-1, 0),  # вверх
            (1, 1),   # по диагонали
            (-1, 1),
            (1, -1),
            (-1, -1)
        ]

    def get_neighbors(self, node: Node) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in self.directions:
            new_pos = (node.position[0] + dx, node.position[1] + dy)
            # Проверка на границы сетки и препятствия
            if (0 <= new_pos[0] < self.grid_size[0] and
                0 <= new_pos[1] < self.grid_size[1] and
                new_pos not in self.obstacles):
                neighbors.append(new_pos)
        return neighbors

    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

    def line_of_sight(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        # Проверяет, есть ли прямая видимость между двумя точками (алгоритм Брезенхэма)
        x0, y0 = p1
        x1, y1 = p2
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        n = 1 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy
        dx *= 2
        dy *= 2

        for _ in range(n):
            if (x, y) in self.obstacles:
                return False
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
        return True

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        # Находит путь от старта до цели с помощью алгоритма Theta*
        start_node = Node(start, 0, self.heuristic(start, end))
        open_set = []
        heapq.heappush(open_set, start_node)
        closed_set = set()
        nodes = {start: start_node}
        while open_set:
            current = heapq.heappop(open_set)
            if current.position == end:
                path = []
                while current:
                    path.append(current.position)
                    current = current.parent
                reversed_path = []
                for i in range(len(path)-1, -1, -1):
                    reversed_path.append(path[i])
                return reversed_path
            closed_set.add(current.position)
            for neighbor_pos in self.get_neighbors(current):
                if neighbor_pos in closed_set:
                    continue
                if neighbor_pos not in nodes:
                    neighbor = Node(neighbor_pos)
                    nodes[neighbor_pos] = neighbor
                else:
                    neighbor = nodes[neighbor_pos]
                if current.parent and self.line_of_sight(current.parent.position, neighbor_pos):
                    parent = current.parent
                    g_cost = parent.g_cost + self.heuristic(parent.position, neighbor_pos)
                else:
                    parent = current
                    g_cost = current.g_cost + self.heuristic(current.position, neighbor_pos)
                if g_cost >= neighbor.g_cost:
                    continue
                neighbor.parent = parent
                neighbor.g_cost = g_cost
                neighbor.h_cost = self.heuristic(neighbor_pos, end)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                found = False
                for n in open_set:
                    if n.position == neighbor_pos:
                        found = True
                        break
                if not found:
                    heapq.heappush(open_set, neighbor)
        return []  # Путь не найден

    def update_obstacles(self, new_obstacles: List[Tuple[int, int]]) -> None:
        self.obstacles = set(new_obstacles) 