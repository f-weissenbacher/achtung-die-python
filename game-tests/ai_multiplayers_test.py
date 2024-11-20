import numpy as np
from game import AchtungDieKurveGame
import logging
import log

from players.aiplayers import RandomSteeringAIPlayer, WallAvoidingAIPlayer, NStepPlanPlayer

import random

#random.seed(1234)

log.setup_colored_logs('info', do_basic_setup=True)

game = AchtungDieKurveGame(mode="gui", target_fps=30)

#game.spawn_player(4, player_type="human", name="fawi")
#game.spawn_player(5, player_type=WallAvoidingAIPlayer, min_turn_radius=game.min_turn_radius)

#game.spawn_player(5, player_type=RandomSteeringAIPlayer)

dist_per_step = 50.
ticks_per_step = int(dist_per_step/game.dist_per_tick)
plan_update_period = int(0.15*ticks_per_step)
for k in range(1,3):
    game.spawn_player(k, player_type=NStepPlanPlayer, name=None, num_steps=3, dist_per_step=dist_per_step,
                      plan_update_period=plan_update_period)

for k in range(3,7):
    game.spawn_player(k, player_type=RandomSteeringAIPlayer)

game.run_game_loop(close_when_finished=True)
game.print_scoreboard()

game.print_timing_stats()
