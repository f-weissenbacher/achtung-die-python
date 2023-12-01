import copy
import itertools
import logging

import matplotlib.pyplot as plt
import pygame
import numpy as np
from players.player_base import PlayerAction, Player
from players.dummy_player import DummyPlayer
from .aiplayer_base import AIPlayer

import shapely

num_update_ticks = 0

def find_nearest_intersection(path1:shapely.LineString, path2:shapely.LineString, calc_dist_along_path2=False):
    intersect = path1.intersection(path2)
    dtc1 = np.nan
    dtc2 = np.nan
    if isinstance(intersect, shapely.Point):
        # dtc == 'distance to conflict'
        dtc1 = path1.line_locate_point(intersect)
        if calc_dist_along_path2:
            dtc2 = path2.line_locate_point(intersect)
    elif isinstance(intersect, shapely.MultiPoint):
        closest_coll_pt = None
        for pt in intersect.geoms:
            dist2pt1= path1.line_locate_point(pt)
            if dist2pt1 < dtc1:
                dtc1 = dist2pt1
                closest_coll_pt = pt

        intersect = closest_coll_pt
        if calc_dist_along_path2:
            dtc2 = path2.line_locate_point(closest_coll_pt)
    else:
        intersect = None

    if calc_dist_along_path2:
        return intersect, dtc1, dtc2
    else:
        return intersect, dtc1


class NStepPlanPlayer(AIPlayer):
    def __init__(self, num_steps=2, dist_per_step=40.0, wall_penalty=100., trail_penalty=111., conflict_penalty=50,
                 discount_factor=0.95, plan_update_period=None, ticks_per_step=None, **aiplayer_kwargs):
        """

        Args:
            num_steps (int): Number of steps (of length dist_per_step) the agent plans into the future
            dist_per_step (float):
            wall_penalty:
            trail_penalty:
            conflict_penalty:
            discount_factor:
            plan_update_period: number of ticks between plan updates. If `plan_update_period` is a float, the number of ticks
                                is calculated as int(plan_update_period * ticks_per_step)
            ticks_per_step (int):
            **aiplayer_kwargs:
        """
        self.N = num_steps
        super().__init__(**aiplayer_kwargs)
        #self.min_turn_radius = min_turn_radius
        self.planned_actions = [PlayerAction.KeepStraight] * 5 # KeepStraight for the next 5 ticks

        if ticks_per_step is not None:
            self.ticks_per_step = ticks_per_step
        else:
        # How far the player travels before it updates its plan
            self.ticks_per_step = int(dist_per_step / self.dist_per_tick)

        if plan_update_period is None:
            plan_update_period = self.N * self.ticks_per_step
        elif isinstance(plan_update_period, float):
            plan_update_period = int(plan_update_period * self.ticks_per_step)
        assert plan_update_period <= self.N * self.ticks_per_step
        assert plan_update_period > 0

        self.plan_update_period = plan_update_period  # Number of ticks between plan updates
        self.ticks_until_next_update = 2
        self.in_planning_tick = False

        # heuristic settings
        self.wall_penalty = wall_penalty
        self.trail_penalty = trail_penalty
        self.conflict_penalty = conflict_penalty
        self.discount_per_tick = discount_factor ** (1/self.plan_update_period)
        self._gamma_vec = np.cumprod([1] + [self.discount_per_tick]*(self.N * self.ticks_per_step))

        self.best_trails = []
        self.collidable_trails = shapely.MultiPolygon()

        self.num_updates = 0


    def __str__(self):
        return f"{self.N}-StepPlanPlayer '{self.name}' ({self.color_name})"


    def next_action(self, game_state):
        # Game is entering the next timestep
        #self.ticks_until_next_update -= 1
        # Check if we should update the plan
        if self.ticks_until_next_update <= 0 or len(self.planned_actions) < 1:
            best_plan = np.asarray(self.find_best_plan(game_state), dtype=PlayerAction)
            self.planned_actions = list(np.repeat(best_plan, self.ticks_per_step))
            self.ticks_until_next_update = self.plan_update_period
            self.in_planning_tick = True
        else:
            self.ticks_until_next_update -= 1
            self.in_planning_tick = False

        return self.planned_actions.pop(0)


    def predict_opponents(self, game_state:dict):
        opponent_futures = []
        for pidx in game_state.keys():
            if pidx == self.idx:
                continue

            trail = game_state[pidx]['trail']
            t_last = np.nanargmax(trail[:,0])
            t_2nd_last = np.nanargmax(trail[:t_last,0])
            pos_2nd_last = trail[t_2nd_last]
            pos_last = trail[t_last]

        return opponent_futures


    def find_best_plan(self, game_state:dict):
        """ Finds the best plan based on the heuristic"""

        #opponent_futures = self.predict_opponents()
        num_own_pos_to_ignore = int(np.ceil(2.5*self.radius/self.dist_per_tick))
        best_plans = []
        best_plan_score = -np.inf
        best_trails = []

        collidable_trails = []
        for pidx,player_state in game_state.items():
            xy = player_state['trail']
            if pidx == self.idx:
                # We need to exclude the last positions from self, otherwise we always detect (self-)collision!
                xy = xy[:-num_own_pos_to_ignore, :]
            if xy.shape[0] >= 2:
                nan_ticks = np.argwhere(np.isnan(xy[:,0])).flatten()
                trail_parts = np.vsplit(xy, nan_ticks)
                if len(trail_parts) == 1:
                    drawn_parts = trail_parts
                else:
                    drawn_parts = []
                    for tp in trail_parts:
                        non_nan_part = tp[~np.isnan(tp[:, 0]), :]
                        if non_nan_part.shape[0] >= 2:
                            drawn_parts.append(non_nan_part)
                #drawn_parts = [tp for tp in trail_parts if not np.any(np.isnan(tp))]
                collidable_trails += drawn_parts

        if len(collidable_trails) > 0:
            #if np.any(np.isinf(collidable_trails)) or np.any(np.isnan(collidable_trails)):
            #    logging.error("NaN of Inf in collidable trails")
            #    raise RuntimeError("NaN of Inf in collidable trails")
            collidable_trails = shapely.geometry.MultiLineString(collidable_trails).buffer(2*self.radius)
            if isinstance(collidable_trails, shapely.Polygon):
                collidable_trails = shapely.MultiPolygon(polygons=[collidable_trails])
            else:
                pass
        else:
            collidable_trails = shapely.geometry.MultiPolygon()


        for action_set in itertools.combinations_with_replacement([PlayerAction.KeepStraight, PlayerAction.SteerLeft, PlayerAction.SteerRight], self.N):
            for plan in set(itertools.permutations(action_set)):
                # for plan in itertools.permutations(action_set):
                #dp = Player(0, "dummy", init_pos=self.pos, init_angle=self.angle, dist_per_tick=self.dist_per_tick*self.ticks_per_step,
                #           startblock_length=np.inf, dphi_per_tick=self.dphi_per_tick*self.ticks_per_step)
                dp = DummyPlayer(init_pos=self.pos, init_angle=self.angle, dist_per_tick=self.dist_per_tick,
                                 startblock_length=np.inf, dphi_per_tick=self.dphi_per_tick)
                plan_score = 0
                # Design of heuristic: Only penalties (negative rewards). As soon as score of current plan
                # drops below score of best plan, we can go to the next one!
                for step_n, a in enumerate(plan):
                    # print(plan)
                    # if a == PlayerAction.SteerLeft:
                    #     steering = {dp.steer_left_key: True, dp.steer_right_key: False}
                    # elif a == PlayerAction.SteerRight:
                    #     steering = {dp.steer_left_key: False, dp.steer_right_key: True}
                    # else:
                    #     steering = {dp.steer_left_key: False, dp.steer_right_key: False}

                    for t in range(step_n*self.ticks_per_step, (step_n+1)*self.ticks_per_step):
                        dp.apply_action(a)
                        dp.move()

                        if not self._pos_inside_bounds(dp.pos, border_width=self.radius):
                            plan_score -= self.wall_penalty * self._gamma_vec[t]

                        if plan_score < best_plan_score:
                            # stop moving dummy player
                            break

                    if plan_score < best_plan_score:
                        # try next plan
                        break

                if plan_score < best_plan_score:
                    # The heuristic score is already below the best plan's, no reason to pursue this plan any further
                    continue

                # Check for collisions with existing trails
                predicted_trail = shapely.LineString(np.array(dp.trail))
                if not collidable_trails.is_empty:
                    for trail in collidable_trails.geoms:
                        intersect, dtc = find_nearest_intersection(predicted_trail, trail)
                        if intersect is not None:
                            # ttc == 'ticks till conflict'
                            ttc = int(dtc / self.dist_per_tick)
                            plan_score -= self.trail_penalty * self._gamma_vec[ttc]
                            # TODO: What if predicted trail hits multiple trails?

                if plan_score > best_plan_score:
                    best_plans = [plan]
                    best_plan_score = plan_score
                    best_trails = [predicted_trail]
                elif plan_score == best_plan_score:
                    best_plans.append(plan)
                    best_trails.append(predicted_trail)

        num_best_plans = len(best_plans)
        if num_best_plans == 0:
            raise RuntimeError(f"Unable to find any plan for {self}!")
        elif num_best_plans == 1:
            best_plan = best_plans[0]
        else:
            logging.debug(f"Found {num_best_plans} equally good plans, selecting one at random")
            best_plan = best_plans[np.random.randint(0,num_best_plans)]

        self.best_trails = best_trails
        self.best_plan_score = best_plan_score
        self.collidable_trails = collidable_trails

        logging.debug(f"Updated N-step plan (score {best_plan_score:.1f}) is: {[s.value for s in best_plan]}")

        return best_plan


    def draw_debug_info(self, surface:pygame.Surface):
        if self.in_planning_tick:
            cmap = plt.get_cmap("Blues")
            norm = plt.Normalize(vmin=-5000, vmax=0)
            self.num_updates += 1
            dbg_color = pygame.Color('dodgerblue')
            dbg_color.a = 150
            pygame.draw.circle(surface=surface, center=self.trail[-2], radius=self.radius+2, color=dbg_color, width=2)

            trails_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

            coll_color = copy.copy(self.color)
            coll_color.a = 60

            #for coll_trail in self.collidable_trails.geoms:
            #    pygame.draw.polygon(trails_surf, color=coll_color, points=coll_trail.exterior.coords, width=0)

            for trail in self.best_trails:
                #pygame.draw.lines(surface, color=dbg_color, points=trail.coords, closed=False, width=2*self.radius )
                trail_color = pygame.Color(np.asarray(cmap(norm(self.best_plan_score))) * 255)
                print(self.best_plan_score)
                pygame.draw.aalines(surface, color=trail_color, points=trail.coords, closed=False)
                #bold_trail = trail.buffer(self.radius).exterior
                #pygame.draw.polygon(trails_surf, color=dbg_color, points=bold_trail.coords, width=0)


            surface.blit(trails_surf, trails_surf.get_rect())
