import math
import random
from typing import List, Tuple, Optional

"""
    # Модуль для генерации шума Перлина и сложных паттернов движения
"""
class PerlinNoise:
    """Класс для генерации шума Перлина (2D)."""
    def __init__(self, seed: int = None):
        """Инициализация генератора шума Перлина."""
        if seed is not None:
            self.seed = seed
        else:
            random.randint(0,1000000)
        random.seed(self.seed)
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p += self.p

    def fade(self, t: float) -> float:
        """Функция сглаживания для интерполяции."""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t: float, a: float, b: float) -> float:
        """Линейная интерполяция."""
        return a + t * (b - a)

    def grad(self, hash: int, x: float, y: float) -> float:
        """Градиентная функция для шума."""
        h = hash & 7
        u = x if h < 4 else y
        v = y if h < 4 else x
        if (h & 1) == 0:
            first_term = u
        else:
            first_term = -u
        if (h & 2) == 0:
            second_term = v
        else:
            second_term = -v
        return first_term + second_term

    def noise(self, x: float, y: float = 0) -> float:
        """Вычисляет значение шума Перлина в точке (x, y)."""
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255

        x -= math.floor(x)
        y -= math.floor(y)

        u = self.fade(x)
        v = self.fade(y)

        A = self.p[X] + Y
        AA = self.p[A]
        AB = self.p[A + 1]
        B = self.p[X + 1] + Y
        BA = self.p[B]
        BB = self.p[B + 1]

        return self.lerp(v,
            self.lerp(u,
                self.grad(self.p[AA], x, y),
                self.grad(self.p[BA], x-1, y)
            ),
            self.lerp(u,
                self.grad(self.p[AB], x, y-1),
                self.grad(self.p[BB], x-1, y-1)
            )
        )

    def octave_noise(self, x: float, y: float, octaves: int, persistence: float = 0.5) -> float:
        """Генерирует фрактальный шум с несколькими октавами."""
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0
        
        for _ in range(octaves):
            total += self.noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2

        return total / max_value

class EnhancedMovementNoise:
    """Класс для генерации сложных паттернов движения врагов с помощью шума Перлина."""
    def __init__(self, seed: int = None):
        """Инициализация параметров движения и генераторов шума."""
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        random.seed(self.seed)
        
        self.base_noise = PerlinNoise(random.randint(0, 1000000))
        self.direction_noise = PerlinNoise(random.randint(0, 1000000))
        self.speed_noise = PerlinNoise(random.randint(0, 1000000))
        self.behavior_noise = PerlinNoise(random.randint(0, 1000000))
        self.spike_noise = PerlinNoise(random.randint(0, 1000000))
        

        self.time = random.random() * 1000
        self.last_direction_change = 0
        self.direction_change_interval = random.randint(60, 180)
        
        self.aggressiveness = random.uniform(0.3, 1.0)
        self.patience = random.uniform(0.5, 1.5)
        self.curiosity = random.uniform(0.2, 0.8)
        
        self.last_offset = (0.0, 0.0)
        self.inertia = random.uniform(0.6, 0.9)

    def get_movement_offset(self, base_direction: Tuple[float, float], 
                          speed: float, level: int = 1, player_pos: Optional[Tuple[float, float]] = None, my_pos: Optional[Tuple[float, float]] = None) -> Tuple[float, float]:
        """Вычисляет смещение для движения врага с учетом уровня и позиции игрока."""
        base_freq = 0.01 + (level * 0.005)
        base_scale = 1.0 + (level * 0.5)
        noise_x = self.base_noise.noise(self.time * base_freq) * base_scale
        noise_y = self.base_noise.noise((self.time + 1000) * base_freq) * base_scale
        dir_freq = 0.005 * self.patience
        dir_x = self.direction_noise.noise(self.time * dir_freq) * 0.5
        dir_y = self.direction_noise.noise((self.time + 500) * dir_freq) * 0.5
        speed_freq = 0.02 * self.aggressiveness
        speed_variation = self.speed_noise.noise(self.time * speed_freq) * 0.3
        behavior_value = self.behavior_noise.noise(self.time * 0.01)
        spike = self.spike_noise.noise(self.time * 0.2)
        if abs(spike) > 0.7:
            noise_x += (random.random() - 0.5) * 8 * (abs(spike) - 0.7)
            noise_y += (random.random() - 0.5) * 8 * (abs(spike) - 0.7)
        if self.aggressiveness > 0.7:
            noise_x *= 0.5
            noise_y *= 0.5
        elif self.curiosity > 0.6:
            noise_x *= 1.5
            noise_y *= 1.5
        if level == 3:
            noise_x += math.sin(self.time * 0.03) * 0.5
            noise_y += math.cos(self.time * 0.03) * 0.5
        elif level == 2:
            noise_x += math.sin(self.time * 0.02) * 0.3
            noise_y += math.cos(self.time * 0.02) * 0.3
        if player_pos is not None and my_pos is not None:
            dx = player_pos[0] - my_pos[0]
            dy = player_pos[1] - my_pos[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist < 200:
                chaos = (200 - dist) / 200
                noise_x += (random.random() - 0.5) * 6 * chaos
                noise_y += (random.random() - 0.5) * 6 * chaos
        final_x = noise_x + dir_x + (behavior_value * 0.2)
        final_y = noise_y + dir_y + (behavior_value * 0.2)
        final_x = self.inertia * self.last_offset[0] + (1 - self.inertia) * final_x
        final_y = self.inertia * self.last_offset[1] + (1 - self.inertia) * final_y
        self.last_offset = (final_x, final_y)
        speed_multiplier = 1.0 + speed_variation
        return final_x * speed_multiplier, final_y * speed_multiplier
    
    def get_behavior_modifier(self) -> float:
        return self.behavior_noise.noise(self.time * 0.005)
    
    def get_aggression_level(self) -> float:
        return self.aggressiveness + (self.behavior_noise.noise(self.time * 0.01) * 0.3)
    
    def update(self):
        self.time += 1
        
        if random.random() < 0.01:
            self.direction_change_interval = random.randint(60, 180)
    
    def get_movement_pattern(self, level: int) -> str:
        behavior = self.get_behavior_modifier()
        aggression = self.get_aggression_level()
        
        if level == 3:
            if aggression > 0.8:
                return "aggressive"
            elif behavior > 0.5:
                return "tactical"
            else:
                return "defensive"
        elif level == 2:
            if aggression > 0.6:
                return "moderate"
            else:
                return "cautious"
        else:
            return "basic"
    
    def get_noise_debug_info(self) -> dict:
        return {
            "base_noise": (
                self.base_noise.noise(self.time * 0.01),
                self.base_noise.noise((self.time + 1000) * 0.01)
            ),
            "direction_noise": (
                self.direction_noise.noise(self.time * 0.005),
                self.direction_noise.noise((self.time + 500) * 0.005)
            ),
            "behavior_value": self.get_behavior_modifier(),
            "aggression": self.get_aggression_level(),
            "personality": {
                "aggressiveness": self.aggressiveness,
                "patience": self.patience,
                "curiosity": self.curiosity
            }
        } 