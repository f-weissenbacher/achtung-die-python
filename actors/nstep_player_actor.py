import pygame
import copy
import numpy as np
import matplotlib.pyplot as plt
from actors.player_actor import PlayerActor
from players.aiplayers import NStepPlanPlayer


class NStepPlanPlayerActor(PlayerActor):

    def __init__(self, nstep_player: NStepPlanPlayer):
        super().__init__(nstep_player)
        self.player = nstep_player

    def draw_debug_info(self, surface: pygame.Surface):
        if self.player.in_planning_tick:
            cmap = plt.get_cmap("Blues")
            norm = plt.Normalize(vmin=-5000, vmax=0)
            self.player.num_updates += 1
            dbg_color = pygame.Color('dodgerblue')
            dbg_color.a = 150
            pygame.draw.circle(surface=surface, center=self.player.trail[-2], radius=self.player.radius+2,
                               color=dbg_color, width=2)

            trails_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

            coll_color = copy.copy(pygame.Color(self.color))
            coll_color.a = 60

            #for coll_trail in self.collidable_trails.geoms:
            #    pygame.draw.polygon(trails_surf, color=coll_color, points=coll_trail.exterior.coords, width=0)

            # DEBUG: Check if trails are correct
            #plt.figure()
            #plt.axis('equal')
            #plt.plot(*self.pos, 'kp')
            #plt.plot(*np.asarray(self.trail[-3:-1]).T, 'k.-')

            for trail in self.player.best_trails:
                #pygame.draw.lines(surface, color=dbg_color, points=trail.coords, closed=False, width=2*self.radius )
                trail_color = pygame.Color(np.asarray(cmap(norm(self.player.best_plan_score))) * 255)
                #print(self.best_plan_score)
                pygame.draw.aalines(surface, color=trail_color, points=trail.coords, closed=False)
                #bold_trail = trail.buffer(self.radius).exterior
                #pygame.draw.polygon(trails_surf, color=dbg_color, points=bold_trail.coords, width=0)

                #plt.plot(*trail.coords.xy, '.-')

            #plt.show(block=True)

            surface.blit(trails_surf, trails_surf.get_rect())
