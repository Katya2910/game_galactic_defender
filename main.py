import pygame
import sys
from src.controllers.game_controller import GameController
from src.controllers.game_loop import cycle_cosmos
from src.config import Config

def main():
    Config.init_assets()
    game = GameController()
    cycle_cosmos(game)

if __name__ == "__main__":
    main()