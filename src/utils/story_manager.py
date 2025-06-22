from typing import Optional

"""
    # Модуль для управления главами и прогрессом сюжетной линии
"""
class StoryManager:
    # Управляет главами и прогрессом сюжетной линии
    def __init__(self):
        self.chapters = [
            "Глава 1: Начало\n\nВаша миссия - защитить Землю от вторжения инопланетян.",
            "Глава 2: Первая волна\n\nРазведчики обнаружили ваш корабль. Будьте осторожны!",
            "Глава 3: Последний шанс\n\nВраг отступает! Добейте их и защитите Землю!",
            "Глава 4: Финальная битва\n\nЭто ваша последняя миссия. Удачи, командир!"
        ]
        self.current_chapter = 0

    def get_current_story(self):
        if self.current_chapter < len(self.chapters):
            return self.chapters[self.current_chapter]
        return None

    def advance_story(self):
        self.current_chapter += 1
        return self.current_chapter < len(self.chapters)

    def reset(self):
        self.current_chapter = 0 