import numpy as np
from game import AchtungDieKurveGame
import logging
import log

from players.aiplayers import RandomSteeringAIPlayer, WallAvoidingAIPlayer, NStepPlanPlayer

import random

#random.seed(1234)

log.setup_colored_logs('debug', do_basic_setup=True)

game = AchtungDieKurveGame(mode="gui-debug", target_fps=20)

#for k in range(1,2):
#    game.spawn_player(k, player_type=RandomSteeringAIPlayer, min_turn_radius=game.min_turn_radius,
#                      turn_angles=np.deg2rad([20.,260.]))

#game.spawn_player(4, player_type="human", name="fawi")
#game.spawn_player(5, player_type=WallAvoidingAIPlayer, min_turn_radius=game.min_turn_radius)

game.spawn_player(5, player_type=RandomSteeringAIPlayer)

dist_per_step = 55.
ticks_per_step = int(dist_per_step/game.dist_per_tick)
plan_update_period = int(0.15*ticks_per_step)
for k in range(1,4):
    game.spawn_player(k, player_type=NStepPlanPlayer, name=None, num_steps=2, dist_per_step=dist_per_step,
                      plan_update_period=plan_update_period)

game.run_game_loop(close_when_finished=False)
game.print_scoreboard()

game.print_timing_stats()
