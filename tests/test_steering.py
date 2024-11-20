import unittest


class TestPlayerSteering(unittest.TestCase):
    def test_circle_motion(self):
        from players.player_base import Player
        import numpy as np

        init_pos = np.array([0., 0.])
        p = Player(1, "manual control", init_pos=init_pos, dist_per_tick=1.0, startblock_length=500.,
                   dphi_per_tick=np.deg2rad(5.0))

        n = int(360 / 5.0)

        steering = {p.steer_left_key: False, p.steer_right_key: True}
        for k in range(n):
            p.apply_steering(steering)
            p.move()

        end_pos = p.pos

        self.assertAlmostEqual(init_pos[0], end_pos[0],
                               msg=f"Loop is not closed: x-position should be {init_pos[0]}, but is {end_pos[0]}")
        self.assertAlmostEqual(init_pos[1], end_pos[1],
                               msg=f"Loop is not closed: x-position should be {init_pos[1]}, but is {end_pos[1]}")


    def test_wave_motion(self):
        from players.player_base import Player
        import numpy as np

        init_pos = (0., 0.)
        p = Player(1, "manual control", init_pos=init_pos, dist_per_tick=1.0, startblock_length=500.,
                   dphi_per_tick=np.deg2rad(5.0), init_angle=np.deg2rad(-45.0))

        n = int(90.0/5.0)

        # Steer right for n timesteps
        steering = {p.steer_left_key: False, p.steer_right_key: True}
        for k in range(n):
            p.apply_steering(steering)
            p.move()

        # steer left for n timesteps
        steering = {p.steer_left_key: True, p.steer_right_key: False}
        for k in range(n):
            p.apply_steering(steering)
            p.move()

        end_pos = (p.pos[0], p.pos[1])
        end_pos_check = (init_pos[0] + 32.3908159, init_pos[1])

        # trail = np.array(p.trail)
        # import matplotlib.pyplot as plt
        # plt.plot(*trail.T, '.-')
        # plt.grid()
        # plt.axis('equal')
        # plt.show()

        self.assertAlmostEqual(end_pos_check[0], end_pos[0], places=5,
                               msg=f"Wave motion: final x-position should be {end_pos_check[0]:.5f}, "
                                   f"but is {end_pos[0]:.5f}")

        self.assertAlmostEqual(end_pos_check[1], end_pos[1], places=5,
                               msg=f"Wave motion: final y-position should be {end_pos_check[1]:.5f}, "
                                   f"but is {end_pos[1]:.5f}")

if __name__ == '__main__':
    unittest.main()
