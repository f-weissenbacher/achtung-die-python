from unittest import TestCase

from develop.predict_trails import dist_per_tick
from game import AchtungDieKurveGame
from players import Player
from players.aiplayers import RandomSteeringAIPlayer

import numpy as np


class TestAchtungDieKurveGame(TestCase):
    def test_repeatability(self):
        rng_seed = 123456

        def setup_and_run_game(seed):
            game = AchtungDieKurveGame(mode="headless", rng_seed=seed, target_fps=10)
            player_kwargs = {"turn_angles_deg": (10., 50.), "straight_lengths": (0, 30.)}
            game.spawn_player(1, player_type=RandomSteeringAIPlayer, **player_kwargs)
            game.spawn_player(2, player_type=RandomSteeringAIPlayer, **player_kwargs)
            for k in range(200):
                game.tick_forward()
            return game.get_game_state()

        game_a_state = setup_and_run_game(rng_seed)
        game_b_state = setup_and_run_game(rng_seed)

        # Compare initial positions & angles
        self.assertTrue(np.allclose(game_a_state[1]['trail'][0], game_b_state[1]['trail'][0]),
                        "Initial positions for player 1 do not match between repeats")
        self.assertTrue(np.allclose(game_a_state[2]['trail'][0], game_b_state[2]['trail'][0]),
                        "Initial positions for player 2 do not match between repeats")

        self.assertAlmostEqual(game_a_state[1]['angles'][0], game_b_state[1]['angles'][0], 6,
                        "Initial angle for player 1 does not match between repeats")
        self.assertAlmostEqual(game_a_state[2]['angles'][0], game_b_state[2]['angles'][0], 6,
                        "Initial angle for player 2 does not match between repeats")

        # Compare trail lengths
        self.assertEqual(len(game_a_state[1]['angles']), len(game_b_state[1]['angles']),
                         "Trail for player 1 not is not the same length")
        self.assertEqual(len(game_a_state[2]['angles']), len(game_b_state[2]['angles']),
                         "Trail for player 2 not is not the same length")

        # Compare full trails and angles for player 1
        self.assertTrue(np.allclose(game_a_state[1]['trail'], game_b_state[1]['trail']),
                        "Trail for player 1 does not match")
        self.assertTrue(np.allclose(game_a_state[1]['angles'], game_b_state[1]['angles']),
                        "Angles for player 1 do not match")

        # Compare trails and angles for player 2
        self.assertTrue(np.allclose(game_a_state[2]['trail'], game_b_state[2]['trail']),
                        "Trail for player 2 does not match")
        self.assertTrue(np.allclose(game_a_state[2]['angles'], game_b_state[2]['angles']),
                        "Angles for player 2 do not match")


    def test_detect_wall_collision(self):
        game = AchtungDieKurveGame(mode="headless")
        sw = game.screen_width
        sh = game.screen_height

        p_out1 = Player(1,"TestPlayer", init_pos=(-50, -30))
        self.assertTrue(game.detect_wall_collision(p_out1))

        p_out2 = Player(1,"TestPlayer", init_pos=(0.5*sw, -30))
        self.assertTrue(game.detect_wall_collision(p_out2))

        p_out3 = Player(1,"TestPlayer", init_pos=(1.2*sw, 1.1*sh))
        self.assertTrue(game.detect_wall_collision(p_out3))

        p_in1 = Player(1,"TestPlayer", init_pos=(0.3*sw, 0.5*sh))
        self.assertFalse(game.detect_wall_collision(p_in1))


    def test_spawn_player(self):
        sw = AchtungDieKurveGame.screen_width
        sh = AchtungDieKurveGame.screen_height

        test_pos = (0.5*sw, 0.7*sh)
        init_angle = 0.5

        game = AchtungDieKurveGame(mode="headless")
        game.spawn_player(1, test_pos, init_angle, Player)
        p1 = Player(1, init_pos=test_pos, init_angle=init_angle)
        player_list = [p1]

        self.assertListEqual(game.players, player_list)
        self.assertListEqual(game.active_players, player_list)
        # Make sure position is correct
        self.assertTrue(np.allclose(p1.pos, game.players[0].pos))
        # Check for correct angle
        self.assertAlmostEqual(p1.angle, game.players[0].angle)

        # Try spawning another player with the same id
        with self.assertRaises(ValueError):
            game.spawn_player(1)

        # Try spawning player outside bounds
        with self.assertRaises(ValueError):
            game.spawn_player(1, init_pos=(1.2*sw, 1.5*sh))

        # Try spawning player on border
        with self.assertRaises(ValueError):
            game.spawn_player(1, init_pos=(0, 0.5*sh))


    def test_initialize_players(self):
        sw = AchtungDieKurveGame.screen_width
        sh = AchtungDieKurveGame.screen_height
        game = AchtungDieKurveGame(mode="headless")

        pos1 = (0.2*sw, 0.3*sh)
        pos2 = (0.4*sw, 0.7*sh)
        pos3 = (0.5*sw, 0.4*sh)
        positions = [pos1, pos2, pos3]

        ids = [1,4,2]
        game.initialize_players(ids, positions)
        self.assertListEqual([game.players[k].idx for k in range(3)], ids)


    def test_move_players(self):
        self.fail()

    def test_tick_forward(self):
        self.fail()

    def test_reverse_tick(self):
        self.fail()
