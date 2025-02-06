"""Multiprocessing Agent Tester Script"""
import copy
import multiprocessing
import time
import numpy as np
import pandas as pd

from adp_game.game import AchtungDieKurveGame

from adp_game.players.aiplayers import NStepPlanPlayer, RandomSteeringAIPlayer


def execute_single_run(game_settings, agent_under_test:dict, opponent_settings:list):

    game = AchtungDieKurveGame(mode='headless', **game_settings)

    # Spawn agent under test
    #player_type = agent_under_test.pop('class')
    game.spawn_player(1, player_type=agent_under_test['type'], name="Agent under Test", **agent_under_test['kwargs'])

    max_idx = min(max(AchtungDieKurveGame.valid_player_ids), len(opponent_settings) + 1)
    for k, idx in enumerate(range(2, max_idx+1)):
        game.spawn_player(idx, player_type=opponent_settings[k]['type'], **opponent_settings[k]['kwargs'])

    # Run game
    game.run_game_loop()

    return game


def benchmark_one_vs_five(num_runs=5, num_workers=4, batch_seed=None):
    game_settings = dict(target_fps=30, game_speed_factor=1.0, run_until_last_player_dies=False,
                     wall_collision_penalty=200., self_collision_penalty=150., player_collision_penalty=100.,
                     survival_reward=100., ignore_self_collisions=False)

    agent_ut_info = {'type': NStepPlanPlayer,
                     'kwargs': dict(num_steps=2, dist_per_step=40.0, plan_update_period=0.15,
                                    wall_penalty=200., trail_penalty=100., conflict_penalty=50., discount_factor=0.9),
                     }


    opponent_settings = [{'type': RandomSteeringAIPlayer,
                          'kwargs': dict(turn_angles_deg=[20.,260.], straight_lengths=(0, 200.0))}] * 4

    t0 = time.time()


    if batch_seed is None:
        # Simplest case: num_runs repetitions of the same settings
        run_settings_batch = [(game_settings, agent_ut_info, opponent_settings)] * num_runs

    else:
        # Extended functionality: set random seeds
        rng = np.random.default_rng(batch_seed)
        rng_seeds = rng.integers(1, 10000, num_runs)
        run_settings_batch = []
        for seed in rng_seeds:
            run_gs = copy.deepcopy(game_settings)
            run_gs["rng_seed"] = seed
            run_settings_batch += [(run_gs, agent_ut_info, opponent_settings)]


    with multiprocessing.Pool(processes=num_workers) as pool:
        finished_games = pool.starmap(execute_single_run, run_settings_batch)

    dt = time.time() - t0
    scoreboards = []
    for run_idx, fg in enumerate(finished_games):
        print(f"==== Run {run_idx+1} ====")
        #print("Initial RNG state: ", fg._init_rng_state)
        if fg.rng_seed is not None:
            print("Initial RNG seed: ", fg.rng_seed)
        fg.print_scoreboard()
        scoreboards.append(fg.scoreboard_as_df())

    # Calculate success statistics for agent under test
    batch_results = pd.concat(scoreboards, join='outer', axis='index',
                              keys=[i+1 for i in range(len(scoreboards))],
                              names=['Run', 'Rank'])

    #print(batch_results)

    # Average scores over multiple
    print()
    aut_results = batch_results.loc[batch_results["Name"].str.contains('Agent under Test')]
    aut_results = aut_results.reset_index()
    print(aut_results)

    aut_averages = aut_results[["Rank", "Score", "Distance", "Total Reward"]].mean()
    aut_averages.rename({"Rank": "Average Rank", "Score": "Average Score", "Distance":"Average Distance",
                                 "Total Reward": "Average Reward"}, inplace=True)
    aut_averages["Win Percentage"] = 100 * np.sum(aut_results["Rank"] == 1) / num_runs
    print()
    print(f"Win-Statistics for Agent under Test of type {agent_ut_info['type']}:")
    print(aut_averages)

    print(f"\nTotal runtime for {num_runs} runs: {dt:.3f} seconds. Time per run {dt/num_runs:.3f} seconds.")
    print(f"Number of workers: {num_workers}")

    return aut_averages["Win Percentage"]



if __name__ == "__main__":
    #np.random.seed(12345)
    benchmark_one_vs_five(num_runs=1000, num_workers=4, batch_seed=12345)









