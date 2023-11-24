import logging
#import random

import numpy as np
seed = np.random.randint(1,20000)
#seed = 16834
#seed = 19421
print("Seed: ", seed)
np.random.seed(seed)


from game import AchtungDieKurveGame
from players.aiplayers import NStepPlanPlayer, WallAvoidingAIPlayer

import pygame


logging.basicConfig(level=logging.INFO,
                    format="%(relativeCreated)d %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=20, game_speed_factor=1.0, run_until_last_player_dies=True,
                           ignore_self_collisions=False, mode="gui-debug")

#print(f"Minimal turning radius: {game.min_turn_radius}")

#game.spawn_player(1, init_pos=(600,400), init_angle=np.deg2rad(60.), player_type=WallAvoidingAIPlayer,
#                  min_turn_radius=game.min_turn_radius, safety_factor=1.05)

# Spawn NStepPlanPlayer
#dist_per_step = 50.
#ticks_per_step = int(dist_per_step/game.dist_per_tick)
#p_ut = game.spawn_player(2, init_pos=(400,200), init_angle=np.deg2rad(0.), player_type=NStepPlanPlayer, num_steps=2,
#                         ticks_per_step=ticks_per_step, startblock_length=50, plan_update_period=int(1.2*ticks_per_step))

dist_per_step = 55.
ticks_per_step = int(dist_per_step/game.dist_per_tick)
p_ut = game.spawn_player(2, init_pos=(400,200), init_angle=np.deg2rad(0.), player_type=NStepPlanPlayer, num_steps=2,
                         ticks_per_step=ticks_per_step, startblock_length=50, plan_update_period=int(1.2*ticks_per_step))

#p_ut = game.players[0] # player under test

# Spawn Wall

#pygame.draw.rect(game.screen, (255,200,0), p1.center_rect, width=1)

#R_min = game.min_turn_radius
#center_rect = pygame.rect.Rect(2*R_min, 2*R_min, game.screen_width - 4*R_min, game.screen_height - 4*R_min)

max_ticks = 50000
tick = 0
game.running = True
while game.running and tick <= max_ticks:
    game.draw_wall_zones()
    #game.draw_debug_info()
    game.flush_display()
    game.tick_forward()
    #p1.draw_turn_circles(game.screen, p1.turn_radius)
    game.flush_display()
    tick += 1

if game.running:
    logging.info(f"SUCCESS: {p_ut} finished without collisions! (seed: {seed})")
else:
    logging.warning(f"FAILURE: {p_ut} hit an obstacle  (seed: {seed})")

logging.info(f"Total travel distance: {p_ut.dist_travelled:.1f}")

print("Number of plan  updates", p_ut.num_updates)

game.running = True
game.wait_for_window_close()

