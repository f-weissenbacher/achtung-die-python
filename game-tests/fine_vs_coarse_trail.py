from players import Player
import numpy as np
import matplotlib.pyplot as plt

dphi_per_tick = np.deg2rad(5.0)

dpt_factor = 6
apt_factor = dpt_factor

p1 = Player(1, "fine stepsize", init_pos=(0, 0), dist_per_tick=1.0, startblock_length=np.inf, dphi_per_tick=dphi_per_tick)

p2 = Player(1, "coarse stepsize", init_pos=(0, 0), dist_per_tick=1.0*dpt_factor, dphi_per_tick=dphi_per_tick*apt_factor,
            startblock_length=np.inf, init_angle=0.0)

steering = {p1.steer_left_key: False, p1.steer_right_key: True}

n1 = int(360/np.rad2deg(p1.dphi_per_tick))
for k in range(n1):
    p1.apply_steering(steering)
    p1.move()

n2 = int(360/np.rad2deg(p2.dphi_per_tick))
for k in range(n2):
    p2.apply_steering(steering)
    p2.move()

#steering = {p.steer_left_key: True, p.steer_right_key: False}
for k in range(1):
    p1.move()
    p2.move()


plt.figure()
plt.plot(*np.array(p1.trail).T, 'o-', fillstyle='none', label=p1.name)
plt.plot(*np.array(p1.trail)[::dpt_factor,:].T, 'ko', fillstyle='none')
plt.plot(*np.array(p2.trail).T, 'o-', fillstyle='none', label=p2.name)
plt.axis('equal')
plt.legend()
plt.grid()

