"""Multiprocessing Agent Tester Script"""
import logging
import multiprocessing
import time

import numpy as np
from game import AchtungDieKurveGame
from players.aiplayers import *

from log import setup_colored_logs

setup_colored_logs(logging.WARNING)



def execute_single_run(game_settings, agent_under_test:dict, opponent_settings:list):

    game = AchtungDieKurveGame(mode='headless', **game_settings)

    # Spawn agent under test
    #player_type = agent_under_test.pop('class')
    game.spawn_player(1, player_type=agent_under_test['type'], name="Agent under Test", **agent_under_test['kwargs'])

    max_idx = min(max(AchtungDieKurveGame.valid_player_indices), len(opponent_settings)+1)
    for k, idx in enumerate(range(2, max_idx+1)):
        game.spawn_player(idx, player_type=opponent_settings[k]['type'], **opponent_settings[k]['kwargs'])

    # Run game
    game.run_game_loop(close_when_finished=True)

    return game

if __name__ == "__main__":

    num_runs = 5

    game_settings = dict(target_fps=30, game_speed_factor=1.0, run_until_last_player_dies=False,
                     wall_collision_penalty=200., self_collision_penalty=150., player_collision_penalty=100.,
                     survival_reward=100., ignore_self_collisions=False, rng_seed=None)

    agent_ut_info = {'type': NStepPlanPlayer,
                     'kwargs': dict(num_steps=2, dist_per_step=40.0, plan_update_period=0.15,
                                    wall_penalty=200., trail_penalty=100., conflict_penalty=50., discount_factor=0.9),
                     }


    opponent_settings = [{'type': RandomSteeringAIPlayer,
                          'kwargs': dict(turn_angles_deg=[20.,260.], straight_lengths=(0, 200.0))}] * 4

    t0 = time.time()


    # Prepare batch of run settings for use with Pool.starmap()
    # Simplest case: num_runs repetitions of the same settings
    run_settings_batch = [(game_settings, agent_ut_info, opponent_settings)] * num_runs

    with  multiprocessing.Pool(processes=2) as pool:
        finished_games = pool.starmap(execute_single_run, run_settings_batch)

    for run_idx, fg in enumerate(finished_games):
        print(f"==== Run {run_idx+1} ====")
        fg.print_scoreboard()

    dt = time.time() - t0
    print(f"\nTotal runtime for {num_runs} runs: {dt:.3f} seconds")









