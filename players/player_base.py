from enum import IntEnum

from players.player_actor import PlayerActor


class PlayerAction(IntEnum):
    SteerLeft = -1
    KeepStraight = 0
    SteerRight = 1

class EvasionTurnState(IntEnum):
    Impossible = 0
    ActionRequired = 1
    Possible = 2

class ReasonOfDeath(IntEnum):
    WallCollision = 0
    SelfCollision = 1
    OpponentCollision = 2


# Import the pygame module
import logging
#import random
import numpy as np

from math import pi, sin, cos, sqrt, ceil

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, idx=1, name=None, init_pos=(0., 0.), init_angle=0.0, dist_per_tick=5.0, dphi_per_tick=0.01, radius=2,
                 color=(255, 10, 10), color_name="Red", steer_left_key=1073741904, steer_right_key=1073741905,
                 hole_width=3.0, startblock_length=100., min_dist_between_holes=200., max_dist_between_holes=1500.,
                 attach_actor=False):
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
            color_name:
            steer_left_key:
            steer_right_key:
            hole_width: width of trail holes in multiples of player diameter
            startblock_length:
            min_dist_between_holes:
            max_dist_between_holes:
        """

        super(Player, self).__init__()
        self.idx = idx
        if name is None:
            self.name = f"{idx:d}"
        else:
            self.name = name

        self.actor = None
        if attach_actor:
            self.attach_actor()

        self.pos = np.array(init_pos, dtype=float)  # x-position in game world (pixel coordinates)
        self.dist_per_tick = dist_per_tick
        self.dphi_per_tick = dphi_per_tick
        self.min_turn_radius = self.dist_per_tick / (2 * sin(0.5*self.dphi_per_tick))
        #self.dphi_per_tick = 2 * asin(self.dist_per_tick / (2 * self.min_turn_radius))
        self.dist_travelled = 0.0  # total distance travelled
        self.total_reward = 0.0 # sum of all rewards, collected by staying alive; collisions add penalties
        self.angle = init_angle  # angle of velocity vector
        self.steer_left_key = steer_left_key
        self.steer_right_key = steer_right_key
        self.color = color
        self.color_name = color_name
        # self.score = 0 # Number of points earned by staying alive

        # Setup sprite == filled circle
        self.radius = int(radius)

        #self.rect = self.brush.get_rect(center=self.pos)
        self.trail = [self.pos.copy()]  # Trail behind player (in cartesian coordinates)
        self.angle_history = [self.angle]

        # Hole settings
        self.hole_width = 2 * self.radius * hole_width  # hole width in game units (px)
        # self.active_hole = False # If true, player does currently draw a "hole" as trail
        self.size_of_active_hole = 0.0
        self.startblock_length = startblock_length  # number of ticks after the start no holes can be activated,
                                                    # set to np.inf to deactivate holes for this player
        self.min_dist_between_holes = min_dist_between_holes
        self.max_dist_between_holes = max_dist_between_holes
        self.dist_to_next_hole = self._roll_dist_to_next_hole()

    def __eq__(self, other):
        return self.idx == other.idx

    def __str__(self):
        return f"Player '{self.name}' ({self.color_name})"

    @property
    def vel_vec(self):
        return self.dist_per_tick * np.asarray([cos(self.angle), sin(self.angle)])

    @property
    def blit_anchor(self):
        return self.pos[0] - self.radius, self.pos[1] - self.radius

    @property
    def active_hole(self):
        return self.dist_to_next_hole <= 0.0

    def attach_actor(self):
        if self.actor is None:
            self.actor = PlayerActor(self)

    def apply_steering(self, pressed_keys):
        # note: this function should only be called once per tick for all regular players
        if pressed_keys[self.steer_left_key]:
            logger.debug(f"{self} steering to the left")
            self.angle -= self.dphi_per_tick
        elif pressed_keys[self.steer_right_key]:
            logger.debug(f"{self} steering to the right")
            self.angle += self.dphi_per_tick

    def _roll_dist_to_next_hole(self):
        if np.isinf(self.startblock_length):
            # Switch off holes
            return np.inf
        if self.dist_travelled < self.startblock_length:
            dist = self.startblock_length + self.max_dist_between_holes * np.random.random()
        else:
            width = self.max_dist_between_holes - self.min_dist_between_holes
            dist = self.min_dist_between_holes + width * np.random.random()

        logger.debug(f"Next hole for {self} in {int(dist / self.dist_per_tick)} ticks")
        return dist

    # move player forward (distance travelled during 1 tick)
    def move(self, log=False):
        dpos = self.vel_vec  # change in position
        self.pos += dpos
        self.dist_travelled += self.dist_per_tick
        self.total_reward += self.dist_per_tick
        self.dist_to_next_hole -= self.dist_per_tick
        # self.rect.move_ip(dx, dy) # update sprite
        if log:
            logger.debug(f"moving {self} by {dpos} to {self.pos}")
        if self.active_hole:
            if log:
                logger.debug(f"active hole for Player {self.idx}")
            self.trail.append(np.array([np.nan] * 2))
            if self.dist_to_next_hole < -self.hole_width:
                # Hole ends with this tick, roll distance to next hole
                self.dist_to_next_hole = self._roll_dist_to_next_hole()
        else:
            self.trail.append(self.pos.copy())  # save updated position in history


    def undo_last_move(self):
        """ Undo the last move. Assumes that no steering has yet been applied in this turn"""
        self.pos -= self.vel_vec
        self.trail.pop(-1)
        self.dist_travelled -= self.dist_per_tick
        self.total_reward -= self.dist_per_tick
        self.dist_to_next_hole += self.dist_per_tick


    def check_self_collision(self):
        num_recent_frames_to_skip = int(ceil(5 * self.radius / self.dist_per_tick))
        logger.debug(f"skipping {num_recent_frames_to_skip} newest frames")
        if len(self.trail) <= num_recent_frames_to_skip:
            return False

        sq_dist = np.sum((np.asarray(self.trail[:-num_recent_frames_to_skip]) - self.pos) ** 2, axis=1)
        frame_collides = sq_dist <= (2 * self.radius) ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logger.debug(f"Collided with own history from frames {np.argwhere(frame_collides).flatten()}")
            return True
        else:
            return False


    def check_player_collision(self, other):
        sq_dist = np.sum((np.asarray(other.trail) - self.pos) ** 2, axis=1)
        frame_collides = sq_dist < self.radius ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logger.debug(
                f"{self} collided with frames {np.argwhere(frame_collides).flatten()} of player {other.idx}")
            return True
        else:
            return False


    def turn_centers(self, turn_radius=None):
        if turn_radius is None:
            turn_radius = self.min_turn_radius

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


    # Drawing Utilities -----------------------
    # each function should call the corresponding functions of the attached PlayerActor, if defined
    def draw(self, surface):
        if self.actor is not None:
            self.actor.draw(surface)

    def draw_debug_info(self, surface):
        if self.actor is not None:
            self.actor.draw_debug_info(surface)

    def draw_turn_circles(self, surface, turn_radius:float):
        if self.actor is not None:
            self.actor.draw_turn_circles(surface, turn_radius)
