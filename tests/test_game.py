from unittest import TestCase

from game import AchtungDieKurveGame
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


