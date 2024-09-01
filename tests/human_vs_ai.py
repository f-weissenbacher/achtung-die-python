import logging
import random
import numpy as np

from game import AchtungDieKurveGame
from players import HumanPlayer
from players.aiplayers import *

import pygame

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=30, game_speed_factor=1.0)
game.ignore_self_collisions = False
game.run_until_last_player_dies = False

print(f"Minimal turning radius: {game.min_turn_radius}")

#game.spawn_player(1, init_pos=(600,400), init_angle=np.deg2rad(60.), player_type=WallAvoidingAIPlayer,
#                  min_turn_radius=game.min_turn_radius, safety_factor=1.05)


game.spawn_player(4,(200,150), np.deg2rad(50), player_type=HumanPlayer, name="human")

enemy_ai_type = "n-step"

if enemy_ai_type == "random":
    # Spawn Random Steering AI players
    for idx in [1,2,3,5]:
         game.spawn_player(idx, init_pos=(random.randrange(50,750),random.randrange(50,550)), init_angle=random.random()*2*np.pi,
                           player_type=RandomSteeringAIPlayer, min_turn_radius=game.min_turn_radius, safety_factor=1.02,
                           turn_angles=np.deg2rad([10,80]), straight_lengths=(50., 200.0))

elif enemy_ai_type == "n-step":
    # Spawn Heuristic-based AI players (N-Step)
    for idx in [1, 2]:
        game.spawn_player(idx, init_pos=(random.randrange(50, 750), random.randrange(50, 550)),
                          init_angle=random.random() * 2 * np.pi,
                          player_type=NStepPlanPlayer, )

#game.running = True
# while game.running:
#     game.draw_wall_zones()
#     game.draw_debug_info()
#     game.flush_display()
#     game.tick_forward(draw=True)
#     #p1.draw_turn_circles(game.screen, p1.turn_radius)
#     game.flush_display()

game.run_game_loop()



