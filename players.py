# Import the pygame module
import logging
import random
import numpy as np

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import pygame
from pygame.locals import RLEACCEL
import pygame.freetype  # Import the freetype module.

from math import pi, sin, cos, sqrt, ceil

from enum import IntEnum

class PlayerAction(IntEnum):
    SteerLeft = -1
    KeepStraight = 0
    SteerRight = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, idx=1, init_pos=(0., 0.), init_angle=0.0, dist_per_tick=5.0, dphi_per_tick=0.01,
                 color=(255, 10, 10), steer_left_key=pygame.K_LEFT, steer_right_key=pygame.K_DOWN,
                 hole_width=3.0, startblock_length=100., min_dist_between_holes=200., max_dist_between_holes=1500.):
        """

        Args:
            idx:
            init_pos:
            init_angle:
            dist_per_tick:
            color:
            steer_left_key:
            steer_right_key:
            hole_width: width of trail holes in multiples of player diameter
        """

        super(Player, self).__init__()
        self.idx = idx
        self.pos = np.asarray(init_pos, dtype=float)  # x-position in game world (pixel coordinates)
        self.dist_per_tick = dist_per_tick
        self.dphi_per_tick = dphi_per_tick
        self.dist_travelled = 0.0  # total distance travelled
        self.angle = init_angle  # angle of velocity vector
        self.steer_left_key = steer_left_key
        self.steer_right_key = steer_right_key
        self.color = color
        # self.score = 0 # Number of points earned by staying alive

        # Setup sprite == filled circle
        self.radius = 3
        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.circle(self.surf, color, (self.radius, self.radius), self.radius, 0)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)  # set transparent color
        self.rect = self.surf.get_rect(center=self.pos)
        self.trail = [self.pos.copy()]  # Trail behind player

        # Hole settings
        self.hole_width = 2 * self.radius * hole_width  # hole width in game units (px)
        # self.active_hole = False # If true, player does currently draw a "hole" as trail
        self.size_of_active_hole = 0.0
        self.startblock_length = startblock_length  # number of ticks after the start no holes can be activated
        self.min_dist_between_holes = min_dist_between_holes
        self.max_dist_between_holes = max_dist_between_holes
        self.dist_to_next_hole = self._roll_dist_to_next_hole()

    def __eq__(self, other):
        return self.idx == other.idx

    def __str__(self):
        return f"Player {self.idx}"

    @property
    def vel_vec(self):
        return self.dist_per_tick * np.asarray([cos(self.angle), sin(self.angle)])

    @property
    def active_hole(self):
        return self.dist_to_next_hole <= 0.0

    def apply_steering(self, pressed_keys):
        if pressed_keys[self.steer_left_key]:
            logging.debug(f"{self} steering to the left")
            self.angle -= self.dphi_per_tick
        elif pressed_keys[self.steer_right_key]:
            logging.debug(f"{self} steering to the right")
            self.angle += self.dphi_per_tick

    def _roll_dist_to_next_hole(self):
        if self.dist_travelled < self.startblock_length:
            dist = self.startblock_length + self.max_dist_between_holes * random.random()
        else:
            width = self.max_dist_between_holes - self.min_dist_between_holes
            dist = self.min_dist_between_holes + width * random.random()

        logging.debug(f"Next hole for {self} in {int(dist / self.dist_per_tick)} ticks")
        return dist

    # move player forward (distance travelled during 1 tick)
    def move(self):
        dpos = self.vel_vec  # change in position
        self.pos += dpos
        self.dist_travelled += self.dist_per_tick
        self.dist_to_next_hole -= self.dist_per_tick
        # self.rect.move_ip(dx, dy) # update sprite
        logging.debug(f"moving {self} by {dpos} to {self.pos}")
        if self.active_hole:
            logging.debug(f"active hole for Player {self.idx}")
            self.trail.append(np.array([np.nan] * 2))
            if self.dist_to_next_hole < -self.hole_width:
                # Hole ends with this tick, roll distance to next hole
                self.dist_to_next_hole = self._roll_dist_to_next_hole()
        else:
            self.trail.append(self.pos.copy())  # save updated position in history

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        if not self.active_hole:
            surface.blit(self.surf, self.pos)

    def check_self_collision(self):
        num_recent_frames_to_skip = int(ceil(5 * self.radius / self.dist_per_tick))
        logging.debug(f"skipping {num_recent_frames_to_skip} newest frames")
        if len(self.trail) <= num_recent_frames_to_skip:
            return False

        sq_dist = np.sum((np.asarray(self.trail[:-num_recent_frames_to_skip]) - self.pos) ** 2, axis=1)
        frame_collides = sq_dist <= (2 * self.radius) ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logging.debug(f"Collided with own history from frames {np.argwhere(frame_collides).flatten()}")
            return True
        else:
            return False

    def check_player_collision(self, other):
        sq_dist = np.sum((np.asarray(other.trail) - self.pos) ** 2, axis=1)
        frame_collides = sq_dist < self.radius ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logging.debug(
                f"{self} collided with frames {np.argwhere(frame_collides).flatten()} of player {other.idx}")
            return True
        else:
            return False


class AIPlayer(Player):
    def __init__(self, game_bounds, **player_kwargs):
        super().__init__(**player_kwargs)

        # bounds of game area [xmin xmax ymin ymax]
        self.xmin, self.xmax, self.ymin, self.ymax = game_bounds

    def next_action(self, game_state):
        """

        Args:
            game_state: a dict that contains the current state of the game (player trails and alive status)

        Returns:
            action: PlayerAction

        """
        raise NotImplementedError

    def get_keypresses(self, game_state):
        """ Query AIPlayer for its next keypresses"""

        action = self.next_action(game_state)

        keypresses = {self.steer_left_key:False, self.steer_right_key:False}
        if action == PlayerAction.SteerLeft:
            keypresses[self.steer_left_key] = True
        elif action == PlayerAction.SteerRight:
            keypresses[self.steer_right_key] = True

        return keypresses

    def _pos_inside_bounds(self, pos):
        return self.xmin <= pos[0] <= self.xmax and self.ymin <= pos[1] <= self.ymax()

    def _dryrun_action(self, action:PlayerAction):
        if action == PlayerAction.SteerLeft:
            new_angle = self.angle - self.dphi_per_tick
        elif action == PlayerAction.SteerRight:
            new_angle = self.angle + self.dphi_per_tick
        else:
            new_angle = self.angle

        return self.pos + self.dist_per_tick * np.array([np.cos(new_angle), np.sin(new_angle)])


    def actions_for_wall_evasion(self, turn_radius):
        actions = [PlayerAction.SteerLeft, PlayerAction.KeepStraight, PlayerAction.SteerRight]

        """ Returns a list of potential PlayerActions for the current tick that hold open wall-evading paths for the player """
        vel_dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        #player_angle = np.mod(self.angle + np.pi, 2*np.pi) - np.pi

        # outward-facing wall normals
        wall_nvecs = np.array([[-1.,0.], [0.,-1.], [1.,0.], [0.,1.]])
        wall_names = np.array(["left","bottom","right","top"])

        # Get distances to walls in case that current heading is kept
        dist_to_left_wall = self.pos[0] - self.xmin
        dist_to_right_wall = self.xmax - self.pos[0]
        dist_to_top_wall = (self.ymax - self.pos[1])  # y-axis is inverted?
        dist_to_bot_wall = (self.pos[1] - self.ymin)  # y-axis is inverted?

        wall_distances = np.array([dist_to_left_wall, dist_to_bot_wall, dist_to_right_wall, dist_to_top_wall])
        logging.debug(f"WallAvoidingPlayer {self.idx} wall distances " + "[{:5.1f} {:5.1f} {:5.1f} {:5.1f}]".format(*wall_distances))

        walls_close = wall_distances <= 2 * turn_radius
        num_walls_close = np.sum(walls_close)

        if num_walls_close == 0:
            # Player in center zone ==> walls pose no restrictions on movement here
            return actions

        # Determine walls that player is currently moving towards (max 2)
        walls_targeted = wall_nvecs.dot(vel_dir.T) >= 0.0

        walls_critical = np.logical_and(walls_close, walls_targeted)
        num_walls_critical = np.sum(walls_critical)

        if num_walls_critical == 0:
            # Player close to one or more walls, but is not moving towards them=> walls only restrict actions if
            # player is very close to one of them
            # Check if the next update would let player collide with walls
            actions = [a for a in actions if self._pos_inside_bounds(self._dryrun_action(a))]
            return actions

        else:
            # One or two walls critical
            R_le = np.array([[0,-1],[1,0]])
            R_ri = np.array([[0,1],[-1,0]])

            forbidden_actions = [PlayerAction.KeepStraight]
            # For each critical wall, check if left and/or right evasion turns are possible
            for wall_idx in np.argwhere(walls_critical):
                dist_to_wall = wall_distances[wall_idx]
                nvec = wall_nvecs[wall_idx]
                if num_walls_close == 1:
                    evec_ri = R_le.dot(nvec.T).flatten()
                    evec_le = R_ri.dot(nvec.T).flatten()
                else:
                    # 2 walls are close -> player is in corner
                    # Player is in one of the corners
                    # evec == escape vector == vector parallel to wall that leads away from the
                    if walls_close[0] and walls_close[1]:
                        # bottom left corner
                        evec_ri = [1., 0.]
                        evec_le = [0., 1.]
                    elif walls_close[1] and walls_close[2]:
                        # bottom right corner
                        evec_ri = [-1.,0.]
                        evec_le = [0., 1.]
                    elif walls_close[2] and walls_close[3]:
                        # top right corner
                        evec_ri = [0.,-1.]
                        evec_le = [-1., 0.]
                    else:
                        # top left corner
                        evec_ri = [1., 0.]
                        evec_le = [0., -1.]

                # Calculate turn angle for left turn
                evasion_turn_angle_le = np.arccos(np.dot(evec_le,vel_dir))
                # Check if evasion turn to the left is possible
                if dist_to_wall < turn_radius * 1 + (np.cos(180 - evasion_turn_angle_le)):
                    logging.debug(f"Unable to evade {wall_names[wall_idx]} wall with left turn")
                    forbidden_actions.append(PlayerAction.SteerLeft)

                # Calculate turn angle for left turn
                evasion_turn_angle_ri = np.arccos(np.dot(evec_ri,vel_dir))
                # Check if evasion turn to the right is possible
                if dist_to_wall < turn_radius * 1 + (np.cos(180 - evasion_turn_angle_ri)):
                    logging.debug(f"Unable to evade {wall_names[wall_idx]} wall with right turn")
                    forbidden_actions.append(PlayerAction.SteerRight)

            return [a for a in actions if a not in forbidden_actions]



class WallAvoidingAIPlayer(AIPlayer):
    def __init__(self,  min_turn_radius, safety_factor=1.02, **aiplayer_kwargs):
        super().__init__(**aiplayer_kwargs)
        #self.min_turn_radius = min_turn_radius
        self.turn_radius = min_turn_radius * safety_factor

    def __str__(self):
        return f"WallAvoidingAIPlayer {self.idx}"

    def next_action(self, game_state):
        possible_actions = self.actions_for_wall_evasion(self.turn_radius)

        if len(possible_actions) == 0:
            logging.debug(f"{self} is unable to evade the walls!")
            return PlayerAction.KeepStraight

        if PlayerAction.KeepStraight in possible_actions:
            # Go straight as long it is possible
            return PlayerAction.KeepStraight
        else:
            # Choose left or right turn at random
            return random.choice(possible_actions)



class RandomSteeringAIPlayer(AIPlayer):
    def __init__(self, turn_angles=(0.2 * pi, 1.5 * pi), straight_lengths=(0, 100.0), **aiplayer_kwargs):
        super().__init__(**aiplayer_kwargs)

        self.turn_angles = turn_angles  # minimum/maximum angle of a turn (in radians)
        self.straight_lengths = straight_lengths  # minimum/maximum distance travelled in straight line (in game units)



