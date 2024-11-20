import logging
import numpy as np
from game import AchtungDieKurveGame
from players.aiplayers import WallAvoidingAIPlayer
import pygame

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=30, game_speed_factor=1.0, run_until_last_player_dies=True)
start_pos = (500,400)
start_angle = 0.0
game.spawn_player(4, start_pos, start_angle)
game.run_game_loop()