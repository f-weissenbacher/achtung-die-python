import logging
import numpy as np

from game import AchtungDieKurveGame
from players import WallAvoidingAIPlayer

import pygame

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=30, game_speed_factor=0.5)

game.spawn_player(1, init_pos=(500 ,100), init_angle=np.deg2rad(10.0), player_type=WallAvoidingAIPlayer,
                  min_turn_radius=game.min_turn_radius, safety_factor=1.1)

p1 = game.players[0]

for k in range(10):
    game.tick_forward(draw=True)
    game.flush_display()


