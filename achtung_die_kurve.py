# Import the pygame module
import logging
import random
import numpy as np

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import pygame
from pygame.locals import RLEACCEL
import pygame.freetype  # Import the freetype module.


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

from math import pi,sin,cos,sqrt, ceil


class Player(pygame.sprite.Sprite):
    def __init__(self, idx=1, init_pos=(0.,0.), init_angle=0.0, speed=100.0, color=(255,10,10),
                 steer_left_key=pygame.K_LEFT, steer_right_key=pygame.K_DOWN):
        super(Player, self).__init__()
        self.idx = idx
        self.pos = np.asarray(init_pos, dtype=float) # x-position in game world (pixel coordinates)
        self.speed = speed # distance travelled per game second
        self.angle = init_angle # angle of velocity vector
        self.steer_left_key = steer_left_key
        self.steer_right_key = steer_right_key
        self.color = color
        #self.score = 0 # Number of points earned by staying alive

        # Setup sprite == filled circle
        self.radius = 4
        self.surf = pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.circle(self.surf, color, (self.radius,self.radius), self.radius, 0)
        self.surf.set_colorkey((0,0,0), RLEACCEL) # set transparent color
        self.rect = self.surf.get_rect(center=self.pos)
        self.history = [self.pos.copy()]

    def __eq__(self, other):
        return self.idx == other.idx

    @property
    def vel_vec(self):
        return self.speed * np.asarray([cos(self.angle), sin(self.angle)])

    def apply_steering(self, pressed_keys, dphi:float):
        if pressed_keys[self.steer_left_key]:
            logging.debug("steering to the left")
            self.angle -= dphi
        elif pressed_keys[self.steer_right_key]:
            logging.debug("steering to the right")
            self.angle += dphi

    # let player move for dt seconds
    def move(self, dt):
        dpos = self.vel_vec * dt # change in position
        self.pos += dpos
        #self.rect.move_ip(dx, dy) # update sprite
        logging.debug(f"moving Player {self.idx} by {dpos} to {self.pos}")
        self.history.append(self.pos.copy()) # save updated position in history

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.surf, self.pos)

    def check_self_collision(self, dt_per_frame):
        num_recent_frames_to_skip = int(ceil(5 * self.radius / (self.speed * dt_per_frame)))
        logging.debug(f"skipping {num_recent_frames_to_skip} newest frames")
        if len(self.history) <= num_recent_frames_to_skip:
            return False

        sq_dist = np.sum((np.asarray(self.history[:-num_recent_frames_to_skip]) - self.pos)**2, axis=1)
        frame_collides = sq_dist < self.radius ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logging.debug(f"Collided with own history from frames {np.argwhere(frame_collides).flatten()}")
            return True
        else:
            return False


    def check_player_collision(self, other):
        sq_dist = np.sum((np.asarray(other.history) - self.pos)**2, axis=1)
        frame_collides = sq_dist < self.radius ** 2
        num_colliding_frames = np.sum(frame_collides)
        if num_colliding_frames > 0:
            logging.debug(f"Player {self.idx} collided with frames {np.argwhere(frame_collides).flatten()} of player {other.idx}")
            return True
        else:
            return False




# Define the enemy object by extending pygame.sprite.Sprite

# The surface you draw on the screen is now an attribute of 'enemy'


class AchtungDieKurveGame:

    player_keys = {1:{'left':pygame.K_LEFT, 'right':pygame.K_DOWN},
                   2:{'left':pygame.K_1, 'right':pygame.K_q}}

    player_colors = {1:(255,10,10), 2:(10,255,10)}

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.player_speed = 0.1 * self.screen_width # pixels travelled per second
        self.min_turn_radius = 0.05 * self.screen_width # minimum turn radius in pixels
        self.spawn_safety_distance = 0.5 * self.min_turn_radius
        #self.min_turn_radius = 100  # minimum turn radius in pixels
        self.player_turn_rate = self.player_speed / self.min_turn_radius # turn rate (radians per second)
        self.players = []
        self.active_players = []
        self.scoreboard = {idx:0 for idx in AchtungDieKurveGame.player_keys}
        #self.winner = None
        self.target_fps = 30
        self.dt_per_frame = 1/self.target_fps
        self.dphi_per_frame = self.player_turn_rate * self.dt_per_frame # maximum steering angle per frame
        #logging.info(f"dphi_per_frame = {self.dphi_per_frame * 180/pi}")
        # Debug flags
        self.run_until_last_player_dies = True

    @staticmethod
    def _roll_random_angle():
        return 2*pi*random.random()

    def _roll_valid_start_position(self, max_attempts=100):
        attempt_counter = 0
        while attempt_counter < max_attempts:
            x = self.min_turn_radius + (self.screen_width - 2 * self.min_turn_radius) * random.random()
            y = self.min_turn_radius + (self.screen_height - 2 * self.min_turn_radius) * random.random()

            for p in self.players:
                dist = sqrt((x - p.pos[0])**2 + (y - p.pos[1])**2)
                if dist < self.spawn_safety_distance:
                    logging.debug("re-rolling start position")
                    break
            else:
                return x,y

            attempt_counter += 1

        raise RuntimeError("Unable to generate valid start position!")


    def detect_wall_collision(self, player:Player):
        x,y = player.pos
        return x <= 0 or x >= self.screen_width or y <= 0 or y >= self.screen_height

    def spawn_player(self, idx, init_pos=None, init_angle=None, color=None):
        if idx in [p.idx for p in self.players]:
            raise ValueError(f"Player {idx} already exists")

        if init_pos is None:
            init_pos = self._roll_valid_start_position()

        if init_angle is None:
            init_angle = self._roll_random_angle()

        if color is None:
            color = self.player_colors[idx]

        p = Player(idx=idx, init_pos=init_pos, speed=self.player_speed, init_angle=init_angle, color=color,
                   steer_left_key=self.player_keys[idx]['left'], steer_right_key=self.player_keys[idx]['right'])

        self.players.append(p)
        self.active_players.append(p)


    def disable_player(self, p):
        """ Remove player from list of active players but keep its history"""
        self.active_players.remove(p)
        # Increment scores of all remaining players
        for op in self.active_players:
            self.scoreboard[op.idx] += 1

        #self.update_scoreboard() # TODO: Create scoreboard display


    def run(self):
        # Initialize pygame
        pygame.init()

        # Fonts
        game_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 30)

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Setup game clock
        clock = pygame.time.Clock()

        # Create custom event for adding a new enemy
        #ADDENEMY = pygame.USEREVENT + 1
        #pygame.time.set_timer(ADDENEMY, 500) # spawn new ENEMIES every X ms

        #screen.fill((255, 255, 255))

        # Create player 1
        self.spawn_player(1, init_pos=(100,400), init_angle=0.0)
        self.spawn_player(2)

        # Variable to keep the main loop running
        running = True
        # Main loop
        frame_num = 0
        while running:
            logging.debug(f">==== Frame {frame_num:d} ===============")
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    running = False

            # Get key presses
            pressed_keys = pygame.key.get_pressed()

            # Refill screen to remove old player/enemy positions
            #screen.fill((0,0,0))

            for p in self.active_players:
                # Process player input
                p.apply_steering(pressed_keys, self.dphi_per_frame)
                # Update player positions
                p.move(self.dt_per_frame)
                # Draw player at its current position
                p.draw(screen)

                # Detect wall collisions
                if self.detect_wall_collision(p):
                    logging.info(f"Player {p.idx} hit the walls")
                    self.disable_player(p)

                # Check self-collision
                elif p.check_self_collision(self.dt_per_frame):
                    logging.info(f"Player {p.idx} collided with itself")
                    self.disable_player(p)

                else:
                    # Check for collision with other players
                    for p2 in self.players:
                        if p == p2:
                            continue
                        elif p.check_player_collision(p2):
                            logging.info(f"Player {p.idx} collided with player {p2.idx}")
                            self.disable_player(p)
                            break

            if len(self.active_players) == 1:
                winner = self.active_players[0]
                win_msg = f"Player {winner.idx} won!"
                logging.info(win_msg)
                game_font.render_to(screen, (int(0.25*SCREEN_WIDTH), int(0.5*SCREEN_HEIGHT)), win_msg, winner.color)
                if not self.run_until_last_player_dies:
                    running = False
            elif len(self.active_players) == 0:
                running = False

            # Render the display (flip everything to the display)
            pygame.display.flip()

            # Ensure program maintains a rate of 30 frames per second
            clock.tick(self.target_fps)
            frame_num += 1

        pygame.time.wait(1500)



if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

    game = AchtungDieKurveGame()
    game.run()

