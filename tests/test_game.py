from unittest import TestCase

from game import AchtungDieKurveGame
from players import Player

from numpy import allclose

class TestAchtungDieKurveGame(TestCase):
    def test_random_seed(self):
        rng_seed = 1234

        game = AchtungDieKurveGame(mode="headless", rng_seed=rng_seed)
        game.initialize_players([1,2])

        p1_reference = Player(1, init_pos=, init_angle=)


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
        self.assertTrue(allclose(p1.pos, game.players[0].pos))
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
