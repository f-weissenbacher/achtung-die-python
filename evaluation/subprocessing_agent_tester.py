"""Agent Tester Script that uses subprocessing"""
import logging
import multiprocessing
import subprocess
import time
import os
import pickle as pkl

import numpy as np
from game import AchtungDieKurveGame
from players.aiplayers import *

from log import setup_colored_logs

setup_colored_logs(logging.WARNING)

import ruamel.yaml as yaml

def run_in_subprocess(run_dir):
    subprocess.run(f"python ./execute_single_run.py {run_dir}", check=True)


if __name__ == "__main__":

    num_runs = 10

    game_settings = dict(target_fps=30, game_speed_factor=1.0, run_until_last_player_dies=False,
                     wall_collision_penalty=200., self_collision_penalty=150., player_collision_penalty=100.,
                     survival_reward=100., ignore_self_collisions=False, rng_seed=12345)

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

    # Prepare run batch folder
    batch_dir = os.path.abspath(os.path.join(".", "run-batch"))
    os.makedirs(batch_dir, exist_ok=True)

    # Create and prepare one folder for each run:
    run_dirs = []
    for run_idx in range(num_runs):
        run_dir = os.path.join(batch_dir, f"run-{run_idx:04d}")
        os.makedirs(run_dir, exist_ok=True)

        # Write run_settings pickle
        with open(os.path.join(run_dir, "run_settings.pkl"),'wb') as rsf:
            pkl.dump({'game_settings': game_settings,
                      'agent_ut_info':agent_ut_info,
                      'opponent_settings':opponent_settings},
                      rsf)

        run_dirs.append((run_dir,))


    with multiprocessing.Pool(processes=4) as pool:
        pool.starmap(run_in_subprocess, run_dirs)


    dt = time.time() - t0
    print(f"\nTotal runtime for {num_runs} runs: {dt:.3f} seconds")









