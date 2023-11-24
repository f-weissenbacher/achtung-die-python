import numpy as np
from players import Player
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import itertools


N = 6
dist_per_tick = 1.0
dphi_per_step = 10
ticks_per_step = 10
dphi_per_tick = dphi_per_step/ticks_per_step

all_trails = []

for action_set in itertools.combinations_with_replacement("LSR",N):
    for plan in set(itertools.permutations(action_set)):
    #for plan in itertools.permutations(action_set):
        p = Player(1, "manual control", init_pos=(0, 0), dist_per_tick=dist_per_tick, startblock_length=500.,
                   dphi_per_tick=np.deg2rad(dphi_per_tick))
        for a in plan:
            #print(plan)
            if a == "L":
                steering = {p.steer_left_key: True, p.steer_right_key: False}
            elif a == "R":
                steering = {p.steer_left_key: False, p.steer_right_key: True}
            else:
                steering = {p.steer_left_key: False, p.steer_right_key: False}

            for k in range(ticks_per_step):
                p.apply_steering(steering)
                p.move()

        all_trails.append(np.array(p.trail))


num_trails = len(all_trails)
num_ticks = N*ticks_per_step
print(f"Number of trails: {num_trails}")

fig, (ax1,ax2) = plt.subplots(nrows=1,ncols=2, figsize=(10,4.5))
#ax1 = fig.add_subplot(111)

for n in range(1,N+1):
    r = dist_per_tick * n * ticks_per_step
    ax1.add_artist(Arc((0,0), width=2*r, height=2*r, theta1=-40., theta2=40., color='m'))

for trail in all_trails:
    ax1.plot(*trail.T, 'C0.-', alpha=0.1)
    ax1.plot(*trail[::ticks_per_step].T,'ko',fillstyle="none", alpha=0.2)

ax1.set_aspect(1.0)
ax1.grid()

# 2d-Histogram


xmin = -1.0
xmax = dist_per_tick*num_ticks
ymax = 25
ymin = -ymax

#hist_tup = ax2.hist2d(all_positions[:,0], all_positions[:,1], bins=31, range=[[xmin, xmax], [ymin, ymax]], density=False)
#ax2.set_aspect(1.0)
#plt.colorbar(ax=ax2, mappable=hist_tup[3])


dx = 0.5
Nx = int((xmax-xmin)/dx)
Ny = int((ymax-ymin)/dx)

smear_sigma = 3.0*dx

xvec = np.linspace(xmin, xmin+Nx*dx, Nx+1)
yvec = np.linspace(ymin, ymin+Ny*dx, Ny+1)

xx,yy = np.meshgrid(xvec, yvec)
hh = np.zeros_like(xx)

A = smear_sigma/(2*np.pi)

hh_t = np.zeros(xx.shape + (num_ticks+1,))
r_t = np.zeros((num_trails, num_ticks+1)) # (r,phi)'s for each timestep
phi_t = np.zeros_like(r_t)
for k,trail in enumerate(all_trails):
    for t,(x0,y0) in enumerate(trail):
        dd_sq = (xx-x0)*(xx-x0) + (yy-y0)*(yy-y0)
        hh_t[:,:,t] += A * np.exp(-0.5*dd_sq/smear_sigma**2)

    r_t[k,:] = np.sqrt(np.sum(trail*trail, axis=1))
    phi_t[k,:] = np.arctan2(trail[:,1], trail[:,0])

# Normalize: sum over smeared positions at specific time must be equal to number of trails

hh_t *= num_trails / np.sum(np.sum(hh_t,axis=0),axis=0)

## Normalize: Total sum should be equal to number of positions
#hh *= len(all_positions)/np.sum(hh)
hh = np.sum(hh_t, axis=2)

#pcm = ax2.pcolormesh(xx,yy, hh, cmap=plt.get_cmap("Blues"))
cmap = plt.get_cmap("viridis")
norm = plt.Normalize(vmin=0, vmax=np.ceil(np.max(hh)))
pcm = ax2.pcolormesh(xx,yy, hh)
ax2.contour(xx,yy,hh, levels=10, colors=["r"])
ax2.set_aspect(1.0)
ax2.grid()
#plt.colorbar(ax=ax2, mappable=pcm)
ax1.set_ylim([ymin,ymax])
ax2.set_ylim([ymin,ymax])

fig.tight_layout()

plt.figure()
ax3d = plt.subplot(111, projection='3d')

ax3d.plot_surface(xx,yy,hh, cmap=cmap, norm=norm)
ax3d.contour(xx,yy,hh, levels=10, colors=["r"])


nrows=2
ncols=5
grid_fig, axes = plt.subplots(2,5, squeeze=True, figsize=(10,8),sharey="row")
keyframes = np.linspace(0, num_ticks, ncols, dtype=int)

frame_norm = plt.Normalize(vmin=0, vmax=1.0)

for k, t in enumerate(keyframes):
    ax = axes[0,k]
    ax.contourf(xx,yy,hh_t[:,:,t], cmap=cmap)
    ax.set_title(f"Tick {t:d}")
    ax.set_aspect(1.0)

    ax2 = axes[1,k]
    ax2.scatter(r_t[:,t] - t*dist_per_tick, np.abs(np.rad2deg(phi_t[:,t])), alpha=0.2)

    ax2.set_xlabel(r"$r - \Delta s\cdot t$")
    if k == 0:
        ax2.set_ylabel(r"$|\varphi - \varphi_0|$")

#grid_fig.tight_layout()








