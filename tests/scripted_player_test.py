import logging
import numpy as np
from game import AchtungDieKurveGame
from players.misc_players import FixedActionListPlayer
import pygame
from players.player_base import PlayerAction

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=10, game_speed_factor=1.0, run_until_last_player_dies=True)

start_pos = (100,100)
start_angle = 0.0

action_list = [PlayerAction.KeepStraight]*20 + [PlayerAction.SteerRight]*15 + [PlayerAction.KeepStraight]*10 + [PlayerAction.SteerLeft]*25

game.spawn_player(4, start_pos, start_angle, player_type=FixedActionListPlayer, action_list=action_list)
game.run_game_loop()