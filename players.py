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

class EvasionTurnState(IntEnum):
    Impossible = 0
    ActionRequired = 1
    Possible = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, idx=1, init_pos=(0., 0.), init_angle=0.0, dist_per_tick=5.0, dphi_per_tick=0.01, radius=2,
                 color=(255, 10, 10), steer_left_key=pygame.K_LEFT, steer_right_key=pygame.K_DOWN,
                 hole_width=3.0, startblock_length=100., min_dist_between_holes=200., max_dist_between_holes=1500.):
        """
        Base class for Achtung,die Kurve players

        Note on pygames coordinate system: origin in top left corner, X points to the right, Y down, Z into the screen
        Therefore, when the angle of a player is increased, its velocity vector rotates in clockwise direction
        (--> the screen is viewed from the negative Z direction!)


        Args:
            idx:
            init_pos: Position of player in cartesian coordinate frame
            init_angle: heading angle of velocity vector, counted from positive x-axis.
            dist_per_tick:
            dphi_per_tick:
            color:
            steer_left_key:
            steer_right_key:
            hole_width: width of trail holes in multiples of player diameter
            startblock_length:
            min_dist_between_holes:
            max_dist_between_holes:
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
        self.radius = int(radius)
        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.circle(self.surf, color, (self.radius, self.radius), self.radius, 0)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)  # set transparent color
        #self.rect = self.surf.get_rect(center=self.pos)
        self.trail = [self.pos.copy()]  # Trail behind player (in cartesian coordinates)

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
    def blit_anchor(self):
        return self.pos[0] - self.radius, self.pos[1] - self.radius

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
            surface.blit(self.surf, self.blit_anchor)

    def draw_debug_info(self, surface):
        """ Draw debug info for player"""
        # Draw velocity vector
        pygame.draw.line(surface, self.color, self.pos, self.pos + self.vel_vec, width=1)

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
        logging.info(f"{self} carries out {action.name}")

        keypresses = {self.steer_left_key:False, self.steer_right_key:False}
        if action == PlayerAction.SteerLeft:
            keypresses[self.steer_left_key] = True
        elif action == PlayerAction.SteerRight:
            keypresses[self.steer_right_key] = True

        return keypresses

    def _pos_inside_bounds(self, pos, border_width=0.0):
        return self.xmin + border_width < pos[0] < self.xmax - border_width and \
               self.ymin + border_width < pos[1] < self.ymax - border_width

    def _dryrun_action(self, action:PlayerAction):
        if action == PlayerAction.SteerLeft:
            new_angle = self.angle - self.dphi_per_tick
        elif action == PlayerAction.SteerRight:
            new_angle = self.angle + self.dphi_per_tick
        else:
            new_angle = self.angle

        return self.pos + self.dist_per_tick * np.array([np.cos(new_angle), np.sin(new_angle)])


    def turn_centers(self, turn_radius):
        w = np.sqrt(turn_radius ** 2 - 0.25 * self.dist_per_tick ** 2)
        # left_turn_state = PlayerTurnState.Possible
        # right_turn_state = PlayerTurnState.Possible

        # prior_pos = self.pos - 0.5 * self.dist_per_tick * vel_dir # distance travelled in prior tick

        turn_centers = {}
        for turn_dir in ["left", "right"]:
            # Vector from halfpoint between current and previous position to center of turning circle
            if turn_dir == "left":
                w_vec = w * np.array([np.cos(self.angle - np.pi / 2), np.sin(self.angle - np.pi / 2)])
            else:
                w_vec = w * np.array([np.cos(self.angle + np.pi / 2), np.sin(self.angle + np.pi / 2)])

            # Center of turn circle
            turn_centers[turn_dir] = self.pos - 0.5 * self.vel_vec + w_vec

        return turn_centers


    def wall_evasion_actions(self, turn_radius, safety_factor=3.0):
        """ Returns a selection of PlayerActions that the player can take and still be able to avoid a wall collision."""
        actions = [PlayerAction.SteerLeft, PlayerAction.KeepStraight, PlayerAction.SteerRight]
        vel_dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        #player_angle = np.mod(self.angle + np.pi, 2*np.pi) - np.pi

        # outward-facing wall normals
        wall_nvecs = np.array([[-1.,0.], [0.,1.], [1.,0.], [0.,-1.]])
        wall_names = np.array(["left","bottom","right","top"])

        # Get distances to walls in case that current heading is kept
        dist_to_left_wall = self.pos[0] - self.xmin
        dist_to_right_wall = self.xmax - self.pos[0]
        dist_to_bot_wall = self.ymax - self.pos[1]  # y-axis is inverted
        dist_to_top_wall = self.pos[1] - self.ymin  # y-axis is inverted

        wall_distances = np.array([dist_to_left_wall, dist_to_bot_wall, dist_to_right_wall, dist_to_top_wall])
        logging.debug(f"WallAvoidingPlayer {self.idx} wall distances " + "[{:5.1f} {:5.1f} {:5.1f} {:5.1f}]".format(*wall_distances))

        walls_close = wall_distances <= 2.5 * turn_radius
        num_walls_close = np.sum(walls_close)

        if num_walls_close == 0:
            # Player in center zone ==> walls pose no restrictions on movement here
            return actions

        # Determine walls that player is currently moving towards (max 2)
        #vel_nvec_sp = wall_nvecs.dot(vel_dir.T)
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
            # Rotation matrices:
            z_veldir = np.exp(1j * self.angle) # complex numbers to the rescue!
            z_dphi_half = np.exp(1j * 0.5 * self.dphi_per_tick)

            w = np.sqrt(turn_radius**2 - 0.25*self.dist_per_tick**2)
            #left_turn_state = PlayerTurnState.Possible
            #right_turn_state = PlayerTurnState.Possible

            #prior_pos = self.pos - 0.5 * self.dist_per_tick * vel_dir # distance travelled in prior tick

            turn_states = {}
            for turn_dir in ["left","right"]:
                # Vector from halfpoint between current and previous position to center of turning circle
                if turn_dir == "left":
                    w_vec = w * np.array([np.cos(self.angle - np.pi/2), np.sin(self.angle - np.pi/2)])
                else:
                    w_vec = w * np.array([np.cos(self.angle + np.pi / 2), np.sin(self.angle + np.pi / 2)])

                # Center of turn circle
                turn_center = self.pos - 0.5 * self.dist_per_tick * vel_dir + w_vec

                # Calculate critical/extremal points on current turning circle
                extremal_points = [turn_center + turn_radius * np.array([-1., 0.]),  # left
                                   turn_center + turn_radius * np.array([0., 1.]),   # bottom (Y-axis is inverted!)
                                   turn_center + turn_radius * np.array([1., 0.]),   # right
                                   turn_center + turn_radius * np.array([0., -1.]),  # top (Y-axis is inverted!)
                                   ]
                extremal_points = np.asarray(extremal_points)

                # Check if turn is possible at the current position
                x_ok = np.logical_and(extremal_points[:,0] > self.xmin, extremal_points[:,0] < self.xmax)
                y_ok = np.logical_and(extremal_points[:,1] > self.ymin, extremal_points[:,1] < self.ymax)
                extrema_in_bounds = np.logical_and(x_ok, y_ok)

                problematic_extrema = np.argwhere(extrema_in_bounds == False).flatten()

                if len(problematic_extrema) > 0:
                    turn_states[turn_dir] = EvasionTurnState.Impossible
                    logging.debug(f"{self} {turn_dir} turn evasion not possible due to conflict with "
                                  f"{wall_names[problematic_extrema]} wall(s)")
                else:
                    turn_states[turn_dir] = EvasionTurnState.Possible

                    # Check if evasion turn would still be possible in the next tick if no action is taken now
                    extremal_points += self.dist_per_tick * vel_dir

                    x_ok = np.logical_and(extremal_points[:, 0] > self.xmin, extremal_points[:, 0] < self.xmax)
                    y_ok = np.logical_and(extremal_points[:, 1] > self.ymin, extremal_points[:, 1] < self.ymax)
                    extrema_in_bounds = np.logical_and(x_ok, y_ok)

                    problematic_extrema = np.argwhere(extrema_in_bounds[walls_critical] == False).flatten()
                    if problematic_extrema.size > 0:
                        turn_states[turn_dir] = EvasionTurnState.ActionRequired
                        logging.debug(f"{self} {turn_dir} turn evasion requires immediate action. conflict with "
                                      f"{wall_names[problematic_extrema]} wall(s) projected for next tick")


            impossible_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.Impossible]
            required_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.ActionRequired]
            possible_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.Possible]

            if len(impossible_turns) == 0:
                # both left and right turn still possible
                # check if both need immediate action
                if len(required_turns) == 2:
                    # Player has to steer to avoid future collision, but the direction is arbitrary
                    actions = [PlayerAction.SteerLeft, PlayerAction.SteerRight]
                else:
                    # At least 1 turn is non-compulsory, player can choose to go straight as well
                    actions = [PlayerAction.SteerLeft, PlayerAction.KeepStraight,PlayerAction.SteerRight]

            elif len(impossible_turns) == 1:
                # One turn is still possible. Check if it requires immediate action
                if len(required_turns) == 0:
                    # Remaining turn is not compulsory.
                    actions = [PlayerAction.SteerLeft if possible_turns[0] == "left" else PlayerAction.SteerRight]

                    # Check if straight action is possible as well
                    if self._pos_inside_bounds(self._dryrun_action(PlayerAction.KeepStraight)):
                        actions.append(PlayerAction.KeepStraight)
                elif len(required_turns) == 1:
                    # Remaining turn is compulsory
                    actions = [PlayerAction.SteerLeft if required_turns[0] == "left" else PlayerAction.SteerRight]
                else:
                    # This should not happen
                    raise RuntimeError("There should not be more than 1 required evasion turn if the other evasion turn is impossible!")

            else:
                # no evasion turns are possible --> player has already failed, will eventually hit the wall
                actions = []


            logging.debug(f"Possible steering actions for wall evasion {actions}")
            return actions


    # DEBUG Utilities ------------------------------
    def draw_turn_circles(self, surface, turn_radius):
        """ draw turn circles for player. left circle yellowish, right circle light blue
        """
        turn_centers = self.turn_centers(turn_radius)

        # left turn circle
        pygame.draw.circle(surface, pygame.Color("goldenrod"), turn_centers['left'], turn_radius, width=1)

        # left turn circle
        pygame.draw.circle(surface, pygame.Color("deepskyblue"), turn_centers['right'], turn_radius, width=1)




class WallAvoidingAIPlayer(AIPlayer):
    def __init__(self,  min_turn_radius, safety_factor=1.05, **aiplayer_kwargs):
        super().__init__(**aiplayer_kwargs)
        #self.min_turn_radius = min_turn_radius
        self.turn_radius = min_turn_radius * safety_factor
        self.center_rect = pygame.rect.Rect(self.xmin + 2*self.turn_radius, self.ymin + 2*self.turn_radius,
                                            (self.xmax - self.xmin) - 4*self.turn_radius,
                                            (self.ymax - self.ymin) - 4*self.turn_radius)


    def __str__(self):
        return f"WallAvoidingAIPlayer {self.idx}"

    def next_action(self, game_state):
        if self.center_rect.collidepoint(*self.pos):
            return PlayerAction.KeepStraight

        possible_actions = self.wall_evasion_actions(self.turn_radius)

        if len(possible_actions) == 0:
            logging.debug(f"{self} is unable to evade the walls!")
            return PlayerAction.KeepStraight

        if PlayerAction.KeepStraight in possible_actions:
            # Go straight as long it is possible
            return PlayerAction.KeepStraight
        else:
            # Choose left or right turn at random
            #return random.choice(possible_actions)
            if PlayerAction.SteerRight in possible_actions:
                return PlayerAction.SteerRight
            else:
                return PlayerAction.SteerLeft



class RandomSteeringAIPlayer(AIPlayer):
    def __init__(self, turn_angles=(0.2 * pi, 1.5 * pi), straight_lengths=(0, 100.0), **aiplayer_kwargs):
        super().__init__(**aiplayer_kwargs)

        self.turn_angles = turn_angles  # minimum/maximum angle of a turn (in radians)
        self.straight_lengths = straight_lengths  # minimum/maximum distance travelled in straight line (in game units)



