import logging
import random

import numpy as np

from game import AchtungDieKurveGame
from players.aiplayers import WallAvoidingAIPlayer, RandomSteeringAIPlayer

import pygame

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=30, game_speed_factor=1.0, run_until_last_player_dies=False,
                           ignore_self_collisions=False, rng_seed=123456)

print(f"Minimal turning radius: {game.min_turn_radius}")

#game.spawn_player(1, init_pos=(600,400), init_angle=np.deg2rad(60.), player_type=WallAvoidingAIPlayer,
#                  min_turn_radius=game.min_turn_radius, safety_factor=1.05)

# Random spawn
game.spawn_player(1, player_type=RandomSteeringAIPlayer)
game.spawn_player(2, player_type=RandomSteeringAIPlayer)

game.run_game_loop()


