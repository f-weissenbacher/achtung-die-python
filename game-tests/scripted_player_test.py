import logging
import numpy as np
from game import AchtungDieKurveGame
from players.misc_players import FixedActionListPlayer
import pygame
from players.player_base import PlayerAction

def discretize_movement_plan(plan, game:AchtungDieKurveGame):
    action_list = []

    for plan_item in plan:
        action = plan_item[0]
        amount = plan_item[1]

        if action == PlayerAction.KeepStraight:
            # amount is length
            action_list += [PlayerAction.KeepStraight] * int(np.round(amount/game.dist_per_tick,0))
        elif action == PlayerAction.SteerLeft or action == PlayerAction.SteerRight:
            # amount is direction change
            action_list += [action] * int(np.round(amount/np.rad2deg(game.dphi_per_tick),0))
        else:
            raise TypeError("Each plan item must be a tuple (PlayerAction, amount)")

    return action_list


logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=20, game_speed_factor=1.0, run_until_last_player_dies=True)

start_pos = (100,100)
start_angle = 0.0

#action_list = [PlayerAction.KeepStraight]*20 + [PlayerAction.SteerRight]*15 + [PlayerAction.KeepStraight]*10 + [PlayerAction.SteerLeft]*25

trajectory_plan = [(PlayerAction.KeepStraight, 200),
                   (PlayerAction.SteerRight, 90.),
                   (PlayerAction.KeepStraight, 50.),
                   (PlayerAction.SteerRight, 60.)]

action_list = discretize_movement_plan(trajectory_plan, game)

game.spawn_player(4, start_pos, start_angle, player_type=FixedActionListPlayer, action_list=action_list)
game.run_game_loop()