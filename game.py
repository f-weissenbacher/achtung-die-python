# Import the pygame module
import logging
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import pygame
from pygame.locals import RLEACCEL
import pygame.freetype  # Import the freetype module.


from math import pi,sqrt, asin

from players import *

# Define the enemy object by extending pygame.sprite.Sprite

# The surface you draw on the screen is now an attribute of 'enemy'


class AchtungDieKurveGame:
    """
    Coordinate system

    o --------- > X
    |
    |
    |
    v
    Y       z-axis points down into screen
    """


    player_keys = {1:{'left':pygame.K_1, 'right':pygame.K_q},
                   2:{'left':pygame.K_x, 'right':pygame.K_c},
                   3:{'left':pygame.K_m, 'right':pygame.K_COMMA},
                   4:{'left':pygame.K_LEFT, 'right':pygame.K_DOWN},
                   5:{'left':pygame.K_KP_DIVIDE, 'right':pygame.K_KP_MULTIPLY},
                   6: {'left': pygame.K_KP0, 'right': pygame.K_KP_PERIOD},
                   }

    player_colors = {1: pygame.Color("red"),
                     2: pygame.Color("yellow"),
                     3: pygame.Color("orange"),
                     4: pygame.Color("lime"),
                     5: pygame.Color("magenta"),
                     6: pygame.Color("turquoise1"),
                     }

    def __init__(self, target_fps=30, game_speed_factor=1.0):
        self.running = False
        self.screen_width = 800
        self.screen_height = 600
        self.game_bounds = [0, self.screen_width, 0, self.screen_height]
        self.min_turn_radius = 0.05 * self.screen_width # minimum turn radius in pixels
        self.spawn_safety_distance = 0.5 * self.min_turn_radius
        #self.min_turn_radius = 100  # minimum turn radius in pixels
        self.player_speed = game_speed_factor * 0.075 * self.screen_width # pixels travelled per second of game time

        self.target_fps = target_fps
        #dt_per_tick = 1/self.target_fps
        self.current_frame = -1 # game has not been started yet
        self.dist_per_tick = self.player_speed/self.target_fps # distance travelled by player during 1 tick
        self.dphi_per_tick = 2*asin(self.dist_per_tick/(2*self.min_turn_radius)) # angle change in randians per tick
        #self.player_turn_rate = self.player_speed / self.min_turn_radius # turn rate (radians per second)
        #logging.info(f"dphi_per_tick = {self.dphi_per_tick * 180/pi}")

        self.players = []
        self.active_players = []
        self.scoreboard = {idx:0 for idx in AchtungDieKurveGame.player_keys}

        # Initialize pygame
        pygame.init()
        # Fonts
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 30)

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Setup game clock
        self.clock = pygame.time.Clock()

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

    def spawn_player(self, idx, init_pos=None, init_angle=None, color=None, player_type=Player, **kwargs):
        if idx in [p.idx for p in self.players]:
            raise ValueError(f"Player {idx} already exists")

        if init_pos is None:
            init_pos = self._roll_valid_start_position()

        if init_angle is None:
            init_angle = self._roll_random_angle()

        if color is None:
            color = self.player_colors[idx]

        player_kwargs = dict(idx=idx, init_pos=init_pos, init_angle=init_angle,
                             dist_per_tick=self.dist_per_tick,
                             dphi_per_tick=self.dphi_per_tick,
                             steer_left_key=self.player_keys[idx]['left'],
                             steer_right_key=self.player_keys[idx]['right'],
                             color=color,
                             )

        if player_type == "human" or player_type == Player:
            p = Player(**player_kwargs)
        elif issubclass(player_type, AIPlayer):
            aiplayer_kwargs = player_kwargs
            aiplayer_kwargs.update(kwargs)
            aiplayer_kwargs['game_bounds'] = self.game_bounds
            if player_type == WallAvoidingAIPlayer:
                p = WallAvoidingAIPlayer(**aiplayer_kwargs)
            elif player_type == RandomSteeringAIPlayer:
                p = RandomSteeringAIPlayer(**aiplayer_kwargs)
            else:
                raise ValueError(f"Invalid AI player type {player_type}")
        else:
            raise ValueError(f"Invalid player type {player_type}")

        self.players.append(p)
        self.active_players.append(p)


    def disable_player(self, p):
        """ Remove player from list of active players but keep its history"""
        self.active_players.remove(p)
        # Increment scores of all remaining players
        for op in self.active_players:
            self.scoreboard[op.idx] += 1

        #self.update_scoreboard() # TODO: Create scoreboard display

    # TODO: implement external tick control

    #def tick(self):
    #    """Advance game by one tick == frame"""
    #
    #    running = True
    #
    #    return running


    def initialize_players(self, player_ids, positions=None):
        if positions is None:
            positions = dict()

        for player_id in player_ids:
            if player_id in positions:
                self.spawn_player(player_id, init_pos=positions[player_id])
            else:
                self.spawn_player(player_id)


    def draw_start_positions(self):
        for p in self.active_players:
            p.draw(self.screen)

        pygame.display.flip()


    def move_players(self, pressed_keys, draw=True):
        """ Advance players by one tick/frame"""
        running = True

        # Refill screen to remove old player/enemy positions
        # screen.fill((0,0,0))

        for p in self.active_players:
            # Process player input
            p.apply_steering(pressed_keys)
            # Update player positions
            p.move()
            # Draw player at its current position
            if draw:
                p.draw(self.screen)

            # Detect wall collisions
            if self.detect_wall_collision(p):
                logging.info(f"Player {p.idx} hit the walls")
                self.disable_player(p)

            # Check self-collision
            elif p.check_self_collision():
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
            if draw:
                self.font.render_to(self.screen, (int(0.25 * self.screen_width), int(0.5 * self.screen_height)), win_msg,
                                winner.color)
            if not self.run_until_last_player_dies:
                running = False
        elif len(self.active_players) == 0:
            running = False

        self.running = running


    def draw_game_state(self):
        """ Draws the current game state"""
        raise NotImplementedError


    def get_game_state(self):
        game_state = {}
        for p in self.players:
            game_state[p.idx] = {'alive': p in self.active_players, 'trail': p.trail}

        return game_state


    def draw_wall_zones(self):
        c = pygame.color.Color("cyan")
        w = 1
        R = self.min_turn_radius
        pygame.draw.line(self.screen, c, (0,2*R),(self.screen_width, 2*R), w)
        pygame.draw.line(self.screen, c, (0, self.screen_height - 2 * R), (self.screen_width, self.screen_height - 2 * R), w)
        pygame.draw.line(self.screen, c, (2*R,0),(2*R, self.screen_height), w)
        pygame.draw.line(self.screen, c, (self.screen_width - 2*R,0), (self.screen_width - 2*R, self.screen_height), w)

        c = pygame.color.Color("green")
        rect = pygame.rect.Rect(R,R,self.screen_width - 2*R, self.screen_height - 2*R)
        pygame.draw.rect(self.screen, c, rect=rect, width=w)


    def draw_debug_info(self):
        # Draw player info
        for ap in self.active_players:
            ap.draw_debug_info(self.screen)

    def tick_forward(self, draw=True):
        """
        Advance game state by one tick
        """
        self.current_frame += 1
        logging.debug(f">==== Frame {self.current_frame:d} ===============")

        # Get key presses
        pressed_keys = pygame.key.get_pressed()

        # Query AI-players for steering input
        for ap in self.active_players:
            if isinstance(ap, AIPlayer):
                ap.apply_steering(ap.get_keypresses(game_state=None))

        self.move_players(pressed_keys, draw=draw)


    def reverse_tick(self):
        "Step back game by 1 tick"

        #for p in self.players:

    def run_game_loop(self):
        self.draw_start_positions()
        # Show Start positions for a short time before starting
        pygame.time.wait(500)

        # Variable to keep the main loop running
        self.running = True
        # Main loop
        while self.running:
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    self.running = False

            if self.running is False:
                logging.info("Game was stopped by user")
                return

            self.draw_wall_zones()
            self.tick_forward()

            # Render the display (flip everything to the display)
            pygame.display.flip()

            # Ensure program maintains a rate of 30 frames per second
            self.clock.tick(self.target_fps)

        pygame.time.wait(1200)


    def flush_display(self, wall_zones=True):
        if wall_zones:
            self.draw_wall_zones()

        pygame.display.flip()


    def wait_for_window_close(self):
        # Main loop
        while self.running:
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    self.running = False

            if self.running is False:
                logging.info("Game was stopped by user")
                return




if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

    game = AchtungDieKurveGame(target_fps=30, game_speed_factor=0.5)
    game.initialize_players([1,2,3,4,5,6])
    game.run_game_loop()

