# Import the pygame module
import logging
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import sys
import time

import pandas as pd
import pygame
import pygame.freetype  # Import the freetype module.

import numpy as np
from math import pi,sqrt, asin

from players.player_base import Player, ReasonOfDeath
from players.human_player import HumanPlayer
from players.aiplayers import AIPlayer, WallAvoidingAIPlayer, RandomSteeringAIPlayer, NStepPlanPlayer
from players.misc_players import ScriptedPlayer, FixedActionListPlayer

# Define the enemy object by extending pygame.sprite.Sprite

import colorama


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

    valid_player_indices = [0, 1, 2, 3, 4, 5, 6]

    player_keys = {0: {'left': pygame.K_F1, 'right': pygame.K_F2}, # virtual player
                   1: {'left': pygame.K_1, 'right': pygame.K_q},
                   2: {'left': pygame.K_x, 'right': pygame.K_c},
                   3: {'left': pygame.K_m, 'right': pygame.K_COMMA},
                   4: {'left': pygame.K_LEFT, 'right': pygame.K_DOWN},
                   5: {'left': pygame.K_KP_DIVIDE, 'right': pygame.K_KP_MULTIPLY},
                   6: {'left': pygame.K_KP0, 'right': pygame.K_KP_PERIOD},
                   }

    #player_ = {0: "Gray", 1: "Red", 2: "Yellow", 3: "Orange", 4: "Green", 5: "Magenta", 6: "Blue"}

    player_colors = {0: ("Gray", pygame.Color('gray')),   # virtual player
                     1: ("Red", pygame.Color("red")),
                     2: ("Yellow", pygame.Color("yellow")),
                     3: ("Orange", pygame.Color("orange")),
                     4: ("Green", pygame.Color("lime")),
                     5: ("Magenta", pygame.Color("magenta")),
                     6: ("Blue", pygame.Color("turquoise1")),
                     }

    bg_color = pygame.Color(30,30,30)

    supported_game_modes = ["gui", "gui-debug", "headless"]

    def __init__(self, mode="gui", target_fps=30., game_speed_factor=1.0, run_until_last_player_dies=False,
                 wall_collision_penalty=200., self_collision_penalty=150., player_collision_penalty=100.,
                 survival_reward=100., ignore_self_collisions=False, rng_seed=None):
        """

        Args:
            target_fps (float):
            game_speed_factor (float):
            run_until_last_player_dies (bool):
            mode (str):
            wall_collision_penalty: float
            self_collision_penalty (float):
            ignore_self_collisions (bool):
            startpos_seed (int):
        """
        if rng_seed is not None:
            np.random.seed(rng_seed)
        self._rng_seed = rng_seed


        if mode in ["gui", "gui-debug", "headless"]:
            self.mode = mode
        else:
            raise ValueError(f"Invalid value '{mode}' selected for game mode. Supported are: {AchtungDieKurveGame.supported_game_modes}.")

        if self.mode == 'headless':
            self.fps_locked = False
        else:
            self.fps_locked = True

        self.running = False
        self.paused = False
        self.screen_width = 800
        self.screen_height = 600
        self.min_turn_radius = 0.05 * self.screen_width # minimum turn radius in pixels
        self.spawn_safety_distance = 0.75 * self.min_turn_radius
        #self.min_turn_radius = 100  # minimum turn radius in pixels
        self.player_speed = game_speed_factor * 0.075 * self.screen_width # pixels travelled per second of game time
        self.player_radius = 2.0
        self.game_bounds = [self.player_radius,
                            self.screen_width - self.player_radius,
                            self.player_radius,
                            self.screen_height - self.player_radius]

        self.target_fps = target_fps
        #dt_per_tick = 1/self.target_fps
        self.current_frame = -1 # game has not been started yet
        self.dist_per_tick = self.player_speed/self.target_fps # distance travelled by player during 1 tick
        self.dphi_per_tick = 2*asin(self.dist_per_tick/(2*self.min_turn_radius)) # angle change in randians per tick
        #self.player_turn_rate = self.player_speed / self.min_turn_radius # turn rate (radians per second)
        #logging.info(f"dphi_per_tick = {self.dphi_per_tick * 180/pi}")

        self.players = []
        self.active_players = []
        self.winner = None
        # Scoring
        self.scoreboard = {idx:0 for idx in AchtungDieKurveGame.player_keys}
        self.wall_collision_penalty = wall_collision_penalty   # subtracted from rewards in case of wall collision
        self.self_collision_penalty = self_collision_penalty   # subtracted from rewards in case of self collision
        self.player_collision_penalty = player_collision_penalty  # subtracted from rewards in case of collision with opponent
        self.survival_reward = survival_reward  # reward for surviving longer than an opponent (awarded when opponent dies)

        # Initialize pygame
        pygame.init()
        # Fonts
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), size=22)
        #self.font = pygame.font.SysFont("Arial", size=30)

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        flags = pygame.HWSURFACE | pygame.SCALED
        if self.mode == 'headless':
            flags |= pygame.HIDDEN
        else:
            flags |= pygame.SHOWN

        self.screen = pygame.display.set_mode(size=(self.screen_width, self.screen_height), flags=flags)
        self.screen.fill(self.bg_color)

        # Setup game clock
        self.clock = pygame.time.Clock()

        # Debug flags
        self.run_until_last_player_dies = run_until_last_player_dies
        self.ignore_self_collisions = ignore_self_collisions

        # Diagnostics
        self.timing_stats = []

        colorama.init()


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
        return x < self.game_bounds[0] or x > self.game_bounds[1] or y < self.game_bounds[2] or y > self.game_bounds[3]

    def spawn_player(self, idx, init_pos=None, init_angle=None, player_type=Player, **kwargs):
        assert idx in self.valid_player_indices

        if idx in [p.idx for p in self.players]:
            raise ValueError(f"Player {idx} already exists")

        if init_pos is None:
            init_pos = self._roll_valid_start_position()

        if init_angle is None:
            init_angle = self._roll_random_angle()

        color_name, color = self.player_colors[idx]

        if not isinstance(color, pygame.Color):
            # The pygame.Color constructor accepts:
            # - a pygame.Color
            # - the name of a color in pygame.colordict.THECOLORS
            # - a RGB tuple
            color = pygame.Color(color)

        player_kwargs = dict(idx=idx, init_pos=init_pos, init_angle=init_angle,
                             dist_per_tick=self.dist_per_tick,
                             dphi_per_tick=self.dphi_per_tick,
                             steer_left_key=self.player_keys[idx]['left'],
                             steer_right_key=self.player_keys[idx]['right'],
                             radius=self.player_radius,
                             color=color, color_name=color_name,
                             )

        if player_type == "human" or player_type in [Player,HumanPlayer]:
            if 'name' not in kwargs:
                kwargs['name'] = 'Unnamed'
            p = HumanPlayer(name=kwargs['name'], **player_kwargs)
        elif issubclass(player_type, ScriptedPlayer):
            scripted_player_kwargs = player_kwargs
            scripted_player_kwargs.update(kwargs)
            if player_type == FixedActionListPlayer:
                p = FixedActionListPlayer(**scripted_player_kwargs)
            else:
                raise ValueError(f"Invalid scripted player type {player_type}")
        elif issubclass(player_type, AIPlayer):
            aiplayer_kwargs = player_kwargs
            aiplayer_kwargs.update(kwargs)
            aiplayer_kwargs['game_bounds'] = self.game_bounds
            if issubclass(player_type, WallAvoidingAIPlayer):
                if 'min_turn_radius' not in aiplayer_kwargs or aiplayer_kwargs['min_turn_radius'] == 'auto':
                    aiplayer_kwargs['min_turn_radius'] = self.min_turn_radius
                if player_type == WallAvoidingAIPlayer:
                    p = WallAvoidingAIPlayer(**aiplayer_kwargs)
                elif player_type == RandomSteeringAIPlayer:
                    p = RandomSteeringAIPlayer(**aiplayer_kwargs)
                else:
                    raise NotImplementedError
            elif player_type == NStepPlanPlayer:
                p = NStepPlanPlayer(**aiplayer_kwargs)
            else:
                raise ValueError(f"Invalid AI player type {player_type}")
        else:
            raise ValueError(f"Invalid player type {player_type}")

        self.players.append(p)
        self.active_players.append(p)

        return p


    def disable_player(self, p, reason:ReasonOfDeath):
        """ Remove player `p` from list of active players but keep its history. Subtracts penalty from that player's
        rewards based on the `reason` of its death, then awards all surviving players a survival bonus"""
        if reason == ReasonOfDeath.SelfCollision:
            p.total_reward -= self.self_collision_penalty
        elif reason == ReasonOfDeath.WallCollision:
            p.total_reward -= self.wall_collision_penalty
        elif reason == ReasonOfDeath.OpponentCollision:
            p.total_reward -= self.player_collision_penalty

        self.active_players.remove(p)
        # Increment scores of all remaining players
        for op in self.active_players:
            self.scoreboard[op.idx] += 1
            op.total_reward += self.survival_reward

        #self.update_scoreboard() # TODO: Create scoreboard display

    # TODO: implement external tick control

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


    def move_players(self, pressed_keys, draw=True, draw_debug=False):
        """ Advance players by one tick/frame

        Returns: timing information
        """
        # Refill screen to remove old player/enemy positions
        # screen.fill((0,0,0))

        timing = {'coll_checks':0., 'draw':0., 'draw_dbg':0.}

        # NOTE: parallelize this?
        for p in self.active_players:
            # Process player input
            p.apply_steering(pressed_keys)
            # Update player positions
            p.move()
            # Draw player at its current position
            if draw:
                t0 = time.time()
                p.draw(self.screen)
                timing['draw'] += time.time() - t0
            if draw_debug:
                t0 = time.time()
                p.draw_debug_info(self.screen)
                timing['draw_dbg'] += time.time() - t0

            t0 = time.time()
            # Detect wall collisions
            if self.detect_wall_collision(p):
                logging.info(f"{p} hit the walls")
                self.disable_player(p, ReasonOfDeath.WallCollision)

            # Check self-collision
            elif p.check_self_collision() and not self.ignore_self_collisions:
                logging.info(f"{p} collided with itself")
                self.disable_player(p, ReasonOfDeath.SelfCollision)

            else:
                # Check for collision with other players
                for p2 in self.players:
                    if p == p2:
                        continue
                    elif p.check_player_collision(p2):
                        logging.info(f"{p} collided with {p2}")
                        self.disable_player(p, ReasonOfDeath.OpponentCollision)
                        break

            timing['coll_checks'] += time.time() - t0

        return timing


    def get_game_state(self):
        game_state = {}
        for p in self.players:
            game_state[p.idx] = {'alive': p in self.active_players,
                                 'trail': np.asarray(p.trail),
                                 'angles': np.asarray(p.angle_history)}

        return game_state

    def save_game_state(self, fp:str, game_state=None):
        import pickle
        if game_state is None:
            game_state = self.get_game_state()
        with open(fp,"wb") as f:
           pickle.dump(game_state, f)

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

    def tick_forward(self):
        """
        Advance game state by one tick

        Return timing info
        """
        self.current_frame += 1
        logging.debug(f">==== Frame {self.current_frame:d} ===============")

        # Get key presses
        pressed_keys = pygame.key.get_pressed()

        # Query AI-players for steering input
        t0_ai = time.time()
        game_state = self.get_game_state()
        for ap in self.active_players:
            if isinstance(ap, AIPlayer):
                steering = ap.get_keypresses(game_state=game_state)
                ap.apply_steering(steering)
        dt_ai = time.time() - t0_ai

        if self.mode == "gui":
            timing = self.move_players(pressed_keys, draw=True, draw_debug=False)
        elif self.mode == "gui-debug":
            timing = self.move_players(pressed_keys, draw=True, draw_debug=True)
        else:
            timing = self.move_players(pressed_keys, draw=False, draw_debug=False)

        timing['ai'] = dt_ai

        if len(self.active_players) == 1:
            self.winner = self.active_players[0]
            if not self.run_until_last_player_dies:
                self.running = False

        elif len(self.active_players) == 0:
            self.running = False

        return timing


    def reverse_tick(self):
        "Step back game by 1 tick"

        for p in self.players:
            p.undo_last_move()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            logging.info("Game paused")
        else:
            logging.info("Game continued")

    def run_game_loop(self, close_when_finished=True):
        self.draw_start_positions()
        # Show Start positions for a short time before starting
        pygame.time.wait(500)

        # Variable to keep the main loop running
        self.running = True
        closed_by_user = False
        # Main game loop
        while self.running:
            ft_t0 = time.time() # frame time timer
            timing = {}
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == pygame.K_ESCAPE:
                        closed_by_user = True
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    closed_by_user = True

            if self.paused:
                # avoid looping too fast while paused
                time.sleep(1/self.target_fps)
                continue

            if closed_by_user:
                logging.info("Game was stopped by user")
                self.running = False
                self.quit()

            if "debug" in self.mode:
                t0 = time.time()
                self.draw_wall_zones()
                timing['draw_dbg'] = time.time() - t0

            # Advance game state by one tick
            tf_timing = self.tick_forward()
            timing.update(tf_timing)

            # Render the display (flip everything to the display)
            t0 = time.time()
            if "gui" in self.mode:
                pygame.display.flip()
            timing['draw'] += time.time() - t0

            if self.fps_locked:
                # Ensure program maintains a target FPS
                self.clock.tick(self.target_fps)
            else:
                self.clock.tick() # used in headless mode

            # frame time: source of FPS calculation
            timing['frame_time'] = time.time() - ft_t0
            self.timing_stats.append(timing)

        # game has finished
        if self.mode == "gui" and self.winner is not None:
            self.show_win_message()

        if close_when_finished:
            if self.mode != 'headless':
                pygame.time.wait(1200)
            self.quit()
        else:
            self.wait_for_window_close()


    def show_win_message(self):
        win_msg = f"{self.winner} won!"
        logging.info(win_msg)
        self.font.render_to(self.screen, (int(0.25 * self.screen_width), int(0.5 * self.screen_height)),
                            text=win_msg, fgcolor=self.winner.color, bgcolor=self.bg_color)
        pygame.display.flip()
        #self.running = False

    def flush_display(self, wall_zones=True):
        if wall_zones:
            self.draw_wall_zones()

        pygame.display.flip()


    def wait_for_window_close(self):
        # Main loop
        wait_for_close = True
        while wait_for_close:
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == pygame.K_ESCAPE:
                        wait_for_close = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    wait_for_close = False

            if wait_for_close is False:
                logging.info("Game window was closed by user")
                self.quit()


    def print_scoreboard(self, pretty=True):
        if pretty:
            sb_dict = {}
            for p in self.players:
                sb_dict[p.idx] = {'Name': str(p), 'Score': self.scoreboard[p.idx], 'Distance': p.dist_travelled,
                                  'Total Reward': p.total_reward}

            scoreboard = pd.DataFrame.from_dict(sb_dict, orient='index')
            scoreboard.sort_values(by='Score', inplace=True, ascending=False)
            scoreboard = scoreboard.reset_index(drop=True)
            scoreboard.index += 1
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                scoreboard_txt = str(scoreboard)

            line_width = scoreboard_txt.index('\n')
            scoreboard_txt = "\n".join(scoreboard_txt.splitlines())
            #print(line_width)
            print("---- Scoreboard " + "-" * max([0, line_width-16]))
            print(scoreboard_txt)
        else:
            print(self.scoreboard)


    def print_timing_stats(self):
        timing_history = pd.DataFrame.from_records(self.timing_stats)

        avg_fps_frametime = 1 / timing_history.frame_time.mean()

        timing_history.drop('frame_time',axis='columns', inplace=True)
        timing_history['total'] = timing_history.sum(axis=1)
        average_times = timing_history.mean(axis=0)
        average_times.sort_values(ascending=False, inplace=True)

        avg_fps_total = 1 / average_times.total

        print("---- Computation Time [ms] per Frame (avg) ----")
        print("\n".join(str(average_times * 1000.).splitlines()[:-1]))
        if self.fps_locked:
            print(f"---- Average FPS (FPS locked, Target: {self.target_fps:.1f}) ----")
        else:
            print("---- Average FPS (FPS not locked) ----")
        print(f"FPS (based on timing total): {avg_fps_total:6.1f}")
        print(f"FPS (based on frame time):   {avg_fps_frametime:6.1f} ")


    def quit(self, force=False):
        if self.running:
            if force:
                logging.warning("Forced 'quit()' was called on game that is still running")
            else:
                logging.warning("Ignoring attempt to quit() called on game that is still running. If you really want to quit "
                                "the game while running==True, use `game.quit(force=True)`.")
                return
        else:
            logging.info("Closing game")

        # Unwind pygame engine
        pygame.display.quit()
        pygame.quit()


    def save_state_to_file(self, fp:str):
        data = {'scoreboard': self.scoreboard, 'trails': {p.idx: p.trail for p in self.players}}

        if fp.endswith('.pkl'):
            import pickle as pkl
            with open(fp, 'wb') as f:
                pkl.dump(data, f)

        else:
            raise NotImplementedError





if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

    game = AchtungDieKurveGame(target_fps=30, game_speed_factor=0.5)
    game.initialize_players([1,2,3,4,5,6])
    game.run_game_loop()

