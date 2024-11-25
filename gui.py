import time

import pygame
import pygame.freetype  # Import the freetype module.

import logging

from players import HumanPlayer
from players.player_base import PlayerAction


class AchtungDieKurveGUI:
    player_keys = {0: {'left': pygame.K_F1, 'right': pygame.K_F2},  # virtual player
                   1: {'left': pygame.K_1, 'right': pygame.K_q},
                   2: {'left': pygame.K_x, 'right': pygame.K_c},
                   3: {'left': pygame.K_m, 'right': pygame.K_COMMA},
                   4: {'left': pygame.K_LEFT, 'right': pygame.K_DOWN},
                   5: {'left': pygame.K_KP_DIVIDE, 'right': pygame.K_KP_MULTIPLY},
                   6: {'left': pygame.K_KP0, 'right': pygame.K_KP_PERIOD},
                   }

    # player_ = {0: "Gray", 1: "Red", 2: "Yellow", 3: "Orange", 4: "Green", 5: "Magenta", 6: "Blue"}

    player_colors = {0: ("Gray", pygame.Color('gray')),  # virtual player
                     1: ("Red", pygame.Color("red")),
                     2: ("Yellow", pygame.Color("yellow")),
                     3: ("Orange", pygame.Color("orange")),
                     4: ("Green", pygame.Color("lime")),
                     5: ("Magenta", pygame.Color("magenta")),
                     6: ("Blue", pygame.Color("turquoise1")),
                     }

    bg_color = pygame.Color(30, 30, 30)


    def __init__(self, game, start_hidden=False):

        self.game = game
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height

        # Initialize pygame
        pygame.init()
        # Fonts
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), size=22)
        #self.font = pygame.font.SysFont("Arial", size=30)

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        flags = pygame.HWSURFACE | pygame.SCALED
        if not start_hidden:
            flags |= pygame.SHOWN

        self.screen = pygame.display.set_mode(size=(self.screen_width, self.screen_height), flags=flags)
        self.screen.fill(self.bg_color)

        # Setup game clock
        self.clock = pygame.time.Clock()


        # color_name, color = self.player_colors[idx]
        #
        # if not isinstance(color, pygame.Color):
        #     # The pygame.Color constructor accepts:
        #     # - a pygame.Color
        #     # - the name of a color in pygame.colordict.THECOLORS
        #     # - a RGB tuple
        #     color = pygame.Color(color)


    def draw_start_positions(self):
        for p in self.game.active_players:
            p.draw(self.screen)

        pygame.display.flip()


    def _parse_human_keypresses(self, pressed_keys):
        """
        Parse PlayerActions for human players based on pressed keys.
        """
        actions = {}
        for p in self.game.active_players:
            if isinstance(p, HumanPlayer):
                if pressed_keys[self.player_keys[p.idx]['left']]:
                    actions[p.idx] = PlayerAction.SteerLeft
                elif pressed_keys[self.player_keys[p.idx]['right']]:
                    actions[p.idx] = PlayerAction.SteerRight
                else:
                    actions[p.idx] = PlayerAction.KeepStraight

        return actions


    def query_human_player_actions(self):
        # Query key presses
        pressed_keys = pygame.key.get_pressed()

        # Start by parsing actions of human players from pressed keys
        actions = self._parse_human_keypresses(pressed_keys)

        return actions


    def draw_wall_zones(self):
        c = pygame.color.Color("cyan")
        w = 1
        R = self.game.min_turn_radius
        pygame.draw.line(self.screen, c, (0,2*R),(self.screen_width, 2*R), w)
        pygame.draw.line(self.screen, c, (0, self.screen_height - 2 * R), (self.screen_width, self.screen_height - 2 * R), w)
        pygame.draw.line(self.screen, c, (2*R,0),(2*R, self.screen_height), w)
        pygame.draw.line(self.screen, c, (self.screen_width - 2*R,0), (self.screen_width - 2*R, self.screen_height), w)

        c = pygame.color.Color("green")
        rect = pygame.rect.Rect(R,R,self.screen_width - 2*R, self.screen_height - 2*R)
        pygame.draw.rect(self.screen, c, rect=rect, width=w)


    def draw_debug_info(self):
        # Draw player info
        for ap in self.game.active_players:
            ap.draw_debug_info(self.screen)


    def show_win_message(self):
        win_msg = f"{self.game.winner} won!"
        logging.info(win_msg)
        self.font.render_to(self.screen, (int(0.25 * self.screen_width), int(0.5 * self.screen_height)),
                            text=win_msg, fgcolor=self.game.winner.color, bgcolor=self.bg_color)
        pygame.display.flip()
        #self.running = False


    def flush_display(self, wall_zones=True):
        if wall_zones:
            self.draw_wall_zones()

        pygame.display.flip()


    def run_game_loop(self, close_when_finished=True):
        self.draw_start_positions()
        # Show Start positions for a short time before starting
        pygame.time.wait(500)

        # Variable to keep the main loop running
        self.game.running = True
        closed_by_user = False
        # Main game loop
        while self.game.running:
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
                        self.game.toggle_pause()

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == pygame.QUIT:
                    closed_by_user = True

            if self.game.paused:
                # avoid looping too fast while paused
                time.sleep(1/self.game.target_fps)
                continue

            if closed_by_user:
                logging.info("Game was stopped by user")
                self.game.running = False
                self.quit()

            if "debug" in self.game.mode:
                t0 = time.time()
                self.draw_wall_zones()
                timing['draw_dbg'] = time.time() - t0

            # Advance game state by one tick
            tf_timing = self.game.tick_forward()
            timing.update(tf_timing)

            # Render the display (flip everything to the display)
            t0 = time.time()
            pygame.display.flip()
            timing['draw'] += time.time() - t0

            if self.game.fps_locked:
                # Ensure program maintains a target FPS
                self.clock.tick(self.game.target_fps)
            else:
                self.clock.tick() # used in headless mode

            # frame time: source of FPS calculation
            timing['frame_time'] = time.time() - ft_t0
            self.game.timing_stats.append(timing)

        # game has finished
        if self.game.winner is not None:
            self.show_win_message()

        if close_when_finished:
            pygame.time.wait(1200)
            self.quit()
        else:
            self.wait_for_window_close()


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


    def quit(self, force=False):
        if self.game.running:
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


