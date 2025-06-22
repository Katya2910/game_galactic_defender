"""
    # Модуль для сохранения и загрузки прогресса игры
"""
import json
import os
from src.config.config import Config

class SaveSystem:
    @staticmethod
    def save_game(data: dict) -> bool:
        # Сохраняет данные игры в файл
        os.makedirs(os.path.dirname(Config.SAVE_FILE), exist_ok=True)
        with open(Config.SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True

    @staticmethod
    def load_game() -> dict:
        # Загружает данные игры из файла
        if os.path.exists(Config.SAVE_FILE):
            with open(Config.SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Значения по умолчанию, если файл не найден
        return {
            "high_score": 0,
            "unlocked_levels": [1]
        } 