from players import Player
import numpy as np
import matplotlib.pyplot as plt

dphi_per_tick = 5.0
ticks_per_action = int(20/dphi_per_tick)
ticks_per_action = 1

trails = {}
for plan in ["LSR","SLL"]:

    p = Player(1, "manual control", init_pos=(0, 0), dist_per_tick=1.0, startblock_length=500.,
               dphi_per_tick=np.deg2rad(dphi_per_tick))

    #for k in range(5):
    #    p.move()

    for a in plan:
        if a == "L":
            steering = {p.steer_left_key: True, p.steer_right_key: False}
        elif a == "R":
            steering = {p.steer_left_key: False, p.steer_right_key: True}
        else:
            steering = {p.steer_left_key: False, p.steer_right_key: False}

        for k in range(ticks_per_action):
            p.apply_steering(steering)
            p.move()

    #for k in range(5):
    #    p.move()

    trails[plan] = np.array(p.trail)

fig = plt.figure()
ax = fig.add_subplot(111)
for plan,trail in trails.items():
    ax.plot(*trail.T, 'o-', fillstyle='none', label=plan)

#ax.set_aspect(1.0)
ax.legend()
ax.grid()
ax.invert_yaxis()

