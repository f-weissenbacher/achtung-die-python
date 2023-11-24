import numpy as np

from game import AchtungDieKurveGame

from players.aiplayers import RandomSteeringAIPlayer, WallAvoidingAIPlayer, NStepPlanPlayer

import random

#random.seed(1234)

game = AchtungDieKurveGame(mode="gui")

#for k in range(1,4):
#    game.spawn_player(k, player_type=RandomSteeringAIPlayer, min_turn_radius=game.min_turn_radius,
#                      turn_angles=np.deg2rad([20.,260.]))

game.spawn_player(4, player_type="human", name="Testuser")
#game.spawn_player(5, player_type=WallAvoidingAIPlayer, min_turn_radius=game.min_turn_radius)
game.spawn_player(6, player_type=NStepPlanPlayer, name="HeuristicAgent", num_steps=2, dist_per_step=55.)

game.run_game_loop(close_when_finished=False)
game.print_scoreboard()
