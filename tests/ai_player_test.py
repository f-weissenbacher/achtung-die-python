import logging
import log
import random

import numpy as np

from game import AchtungDieKurveGame
from players.aiplayers import WallAvoidingAIPlayer

import pygame

log.setup_colored_logs(logging.DEBUG, do_basic_setup=True)

game = AchtungDieKurveGame(target_fps=5, game_speed_factor=1.0, run_until_last_player_dies=True, mode="gui")

print(f"Minimal turning radius: {game.min_turn_radius}")

#game.spawn_player(1, init_pos=(600,400), init_angle=np.deg2rad(60.), player_type=WallAvoidingAIPlayer,
#                  min_turn_radius=game.min_turn_radius, safety_factor=1.05)

# Random spawn
game.spawn_player(1, init_pos=(random.randrange(50,750),random.randrange(50,550)), init_angle=random.random()*2*np.pi, player_type=WallAvoidingAIPlayer,
                  min_turn_radius=game.min_turn_radius, safety_factor=1.02)

p1 = game.players[0]

#pygame.draw.rect(game.screen, (255,200,0), p1.center_rect, width=1)

R_min = game.min_turn_radius
center_rect = pygame.rect.Rect(2*R_min, 2*R_min, game.screen_width - 4*R_min, game.screen_height - 4*R_min)

if center_rect.collidepoint(*p1.pos):
    while center_rect.collidepoint(*p1.pos):
        game.draw_debug_info()
        game.tick_forward()
else:
    logging.info(f"{p1} not spawned in center rect!")

game.flush_display()

max_ticks = 1000
tick = 0
game.running = True
while game.running and tick <= max_ticks:
    game.draw_wall_zones()
    game.draw_debug_info()
    game.flush_display()
    game.tick_forward()
    #p1.draw_turn_circles(game.screen, p1.turn_radius)
    game.flush_display()
    tick += 1

if game.running:
    logging.info(f"SUCCESS: {p1} finished without wall collisions!")

game.running = True
game.wait_for_window_close()


