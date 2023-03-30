import numpy as np

from game import AchtungDieKurveGame

from players import RandomSteeringAIPlayer, WallAvoidingAIPlayer

import random

#random.seed(1234)

game = AchtungDieKurveGame()

for k in range(1,4):
    game.spawn_player(k, player_type=RandomSteeringAIPlayer, min_turn_radius=game.min_turn_radius,
                      turn_angles=np.deg2rad([20.,260.]))

game.spawn_player(4)
game.spawn_player(5, player_type=WallAvoidingAIPlayer, min_turn_radius=game.min_turn_radius)

game.run_game_loop()
game.print_scoreboard()