import argparse
import os
import pickle as pkl

def run_game(game_settings:dict, agent_ut_info:dict, opponent_settings:list):
    from game import AchtungDieKurveGame
    game = AchtungDieKurveGame(mode='headless', **game_settings)

    # Spawn agent under test
    #player_type = agent_under_test.pop('class')
    game.spawn_player(1, player_type=agent_ut_info['type'], name="Agent under Test", **agent_ut_info['kwargs'])

    max_idx = min(max(AchtungDieKurveGame.valid_player_indices), len(opponent_settings)+1)
    for k, idx in enumerate(range(2, max_idx+1)):
        game.spawn_player(idx, player_type=opponent_settings[k]['type'], **opponent_settings[k]['kwargs'])

    # Run game
    game.run_game_loop(close_when_finished=True)

    return game

parser = argparse.ArgumentParser()

parser.add_argument("run_dir")

args = parser.parse_args()

run_dir = os.path.normpath(args.run_dir)

if not os.path.isdir(run_dir):
    raise FileNotFoundError(f"Run folder '{run_dir}' does not exist. Aborting.")

# Make sure that the following files exist: game_settings.yaml, agent_ut_info.yaml
folder_list = os.listdir(run_dir)
if "run_settings.pkl" in folder_list:
    with open(os.path.join(run_dir, "run_settings.pkl"),'rb') as rsf:
        run_settings = pkl.load(rsf)

elif ("game_settings.yml" in folder_list) and ("agent_ut.yml" in folder_list) and ("opponent_settings.yml" in folder_list):
    raise NotImplementedError()

else:
    raise FileNotFoundError("Run settings not found")


finished_game = run_game(**run_settings)

finished_game.save_state_to_file(os.path.join(run_dir, "end_state.pkl"))



