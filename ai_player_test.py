import logging
import numpy as np

from game import AchtungDieKurveGame
from players import WallAvoidingAIPlayer

import pygame

logging.basicConfig(level=logging.DEBUG,
                    format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

game = AchtungDieKurveGame(target_fps=5, game_speed_factor=1.0)

game.spawn_player(1, init_pos=(705,200), init_angle=np.deg2rad(10.0), player_type=WallAvoidingAIPlayer,
                  min_turn_radius=game.min_turn_radius, safety_factor=1.05)

p1 = game.players[0]

R_min = game.min_turn_radius
center_rect = pygame.rect.Rect(2*R_min, 2*R_min, game.screen_width - 4*R_min, game.screen_height - 4*R_min)

while center_rect.collidepoint(*p1.pos):
    game.draw_debug_info()
    game.tick_forward(draw=True)

game.flush_display()

while game.running:
    game.draw_wall_zones()
    game.draw_debug_info()
    game.flush_display()
    game.tick_forward(draw=True)
    game.flush_display()

game.running = True
game.wait_for_window_close()


