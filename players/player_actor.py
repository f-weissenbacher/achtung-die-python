# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import pygame
from pygame.locals import RLEACCEL
import pygame.freetype  # Import the freetype module.

from players.player_base import Player

class PlayerActor(pygame.sprite.Sprite):

    def __init__(self, player:Player):
        super(PlayerActor, self).__init__()

        self.player = player
        self.color = self.player.color

        self.brush = pygame.Surface((2 * self.player.radius, 2 * self.player.radius))
        pygame.draw.circle(self.brush, self.player.color, (self.player.radius, self.player.radius), self.radius, 0)
        self.brush.set_colorkey((0, 0, 0), RLEACCEL)  # set transparent color


    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        if not self.player.active_hole:
            surface.blit(self.brush, self.player.blit_anchor)

    def draw_debug_info(self, surface):
        """ Draw debug info for player"""
        # Draw velocity vector
        pos = self.player.pos
        vel_vec = self.player.vel_vec
        pygame.draw.line(surface, self.color, pos, pos + vel_vec, width=1)


    # DEBUG Utilities ------------------------------
    def draw_turn_circles(self, surface, turn_radius=None):
        """ draw turn circles for player. left circle yellowish, right circle light blue
        """
        if turn_radius is None:
            turn_radius = self.player.min_turn_radius

        turn_centers = self.player.turn_centers(turn_radius)

        # left turn circle
        pygame.draw.circle(surface, pygame.Color("goldenrod"), turn_centers['left'], turn_radius, width=1)

        # left turn circle
        pygame.draw.circle(surface, pygame.Color("deepskyblue"), turn_centers['right'], turn_radius, width=1)