from players import Player
import numpy as np
import matplotlib.pyplot as plt

p = Player(1, "manual control", init_pos=(0, 0), dist_per_tick=1.0, startblock_length=500., dphi_per_tick=np.deg2rad(5.0))

n = int(360/5.0)

steering = {p.steer_left_key: False, p.steer_right_key: True}
for k in range(n):
    p.apply_steering(steering)
    p.move()

#steering = {p.steer_left_key: True, p.steer_right_key: False}
for k in range(10):
    p.move()


plt.figure()
plt.plot(*np.array(p.trail).T, 'o-', fillstyle='none')
plt.axis('equal')
plt.grid()

