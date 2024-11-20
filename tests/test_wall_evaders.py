from unittest import TestCase

from game import AchtungDieKurveGame
from players.aiplayers import WallAvoidingAIPlayer
import numpy as np

from players.player_base import PlayerAction


def mock_game_state(p:WallAvoidingAIPlayer):
    game_state = dict()
    game_state[p.idx] = {'alive': True,
                         'trail': np.asarray(p.trail),
                         'angles': np.asarray(p.angle_history)}
    return game_state

class TestWallAvoidingAIPlayer(TestCase):
    def test_next_action(self):
        self.skipTest("not implemented yet")
        # game_bounds = (0, 800, 0, 600)
        #
        # turn_radius = 50.
        # init_pos1 = (750., turn_radius + 15.0)
        # init_angle1 = np.deg2rad(-60.0)
        # p1 = WallAvoidingAIPlayer(init_pos=init_pos1, init_angle=init_angle1, dist_per_tick=10.0, startblock_length=500.,
        #                           game_bounds=game_bounds, min_turn_radius=turn_radius)

        #self.fail()

    def test_wall_evasion_actions_away_from_border(self):
        game_bounds = (0, 800, 0, 600)
        turn_radius = 50.

        # 1) Away from border
        p1 = WallAvoidingAIPlayer(init_pos= (500., 300.), init_angle=np.deg2rad(-60.0), dist_per_tick=10.0, startblock_length=500.,
                                  game_bounds=game_bounds, min_turn_radius=turn_radius)

        we_actions1 = p1.wall_evasion_actions(turn_radius)
        self.assertListEqual(we_actions1, [PlayerAction.SteerLeft, PlayerAction.KeepStraight, PlayerAction.SteerRight])

    def test_wall_evasion_actions_approaching_border(self):
        game_bounds = (0, 800, 0, 600)
        turn_radius = 50.
        # 2) Start towards top border, agent should be able to go right
        p2 = WallAvoidingAIPlayer(init_pos=(600, turn_radius - 5.0), init_angle=np.deg2rad(-80.0), dist_per_tick=10.0,
                                  startblock_length=500., game_bounds=game_bounds, min_turn_radius=turn_radius)

        we_actions2 = p2.wall_evasion_actions(turn_radius)
        self.assertListEqual(we_actions2, [PlayerAction.SteerRight])

    def test_wall_evasion_actions_facing_border(self):
        game_bounds = (0, 800, 0, 600)
        turn_radius = 50.
        # 2) Start towards top border, agent should be able to go right
        p = WallAvoidingAIPlayer(init_pos=(600, turn_radius + 5.0), init_angle=np.deg2rad(-90.0), dist_per_tick=10.0,
                                  startblock_length=500., game_bounds=game_bounds, min_turn_radius=turn_radius)

        we_actions = p.wall_evasion_actions(turn_radius)
        self.assertListEqual(we_actions, [PlayerAction.SteerLeft, PlayerAction.SteerRight])



    def test_long_run(self):
        self.skipTest("not implemented yet")
        #self.fail()
