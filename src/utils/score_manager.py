"""
Модуль для управления очками и рекордами игрока
"""
import json
import os
from src.config.config import Config
from src.utils.save_system import SaveSystem

class ScoreManager:
    # Управляет текущим счётом и рекордом игрока (Singleton)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
            cls._instance.score = 0
            saved_data = SaveSystem.load_game()
            cls._instance.high_score = saved_data.get("high_score", 0)
        return cls._instance

    def add_score(self, points: int) -> None:
        # Добавляет очки и обновляет рекорд при необходимости
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            SaveSystem.save_game({"high_score": self.high_score})

    def reset_score(self) -> None:
        self.score = 0

    def get_score(self) -> int:
        return self.score

    def get_high_score(self) -> int:
        return self.high_score

    def _load_high_score(self) -> int:
        # Внутренний метод загрузки рекорда из файла
        with open(os.path.join(Config.ASSETS_DIR, "high_score.json"), "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)

    def _save_high_score(self) -> None:
        # Внутренний метод сохранения рекорда в файл
        os.makedirs(Config.ASSETS_DIR, exist_ok=True)
        with open(os.path.join(Config.ASSETS_DIR, "high_score.json"), "w") as f:
            json.dump({"high_score": self.high_score}, f) 