import logging

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import time
import pandas as pd
import numpy as np
from math import pi, sqrt, asin

from collections import defaultdict

from adp_game.players.player_base import Player, ReasonOfDeath, PlayerAction
from adp_game.players.human_player import HumanPlayer
from adp_game.players.aiplayers import AIPlayer, WallAvoidingAIPlayer, RandomSteeringAIPlayer, NStepPlanPlayer
from adp_game.players.misc_players import ScriptedPlayer, FixedActionListPlayer

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

    valid_player_ids = [0, 1, 2, 3, 4, 5, 6]

    player_color_names = {0:"Gray", 1:"Red", 2:"Yellow", 3:"Orange", 4:"Green", 5:"Magenta", 6:"Blue"}

    supported_game_modes = ["gui", "gui-debug", "headless"]

    screen_width = 800
    screen_height = 600

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
            rng_seed (int):
        """

        self.rng = np.random.default_rng(rng_seed)
        self._init_rng_state = self.rng.__getstate__()
        self.rng_seed = rng_seed

        if mode in ["gui", "gui-debug", "headless"]:
            self.mode = mode
        else:
            raise ValueError(f"Invalid value '{mode}' selected for game mode. Supported are: {AchtungDieKurveGame.supported_game_modes}.")

        self.running = False
        self.paused = False
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
        self.current_frame = -1  # game has not been started yet
        self.dist_per_tick = self.player_speed/self.target_fps # distance travelled by player during 1 tick
        self.dphi_per_tick = 2*asin(self.dist_per_tick/(2*self.min_turn_radius)) # angle change in randians per tick
        #self.player_turn_rate = self.player_speed / self.min_turn_radius # turn rate (radians per second)
        #logging.info(f"dphi_per_tick = {self.dphi_per_tick * 180/pi}")

        self.players = []
        self.active_players = []
        self.winner = None
        # Scoring
        self.scoreboard = {idx:0 for idx in AchtungDieKurveGame.valid_player_ids}
        self.wall_collision_penalty = wall_collision_penalty   # subtracted from rewards in case of wall collision
        self.self_collision_penalty = self_collision_penalty   # subtracted from rewards in case of self collision
        self.player_collision_penalty = player_collision_penalty  # subtracted from rewards in case of collision with opponent
        self.survival_reward = survival_reward  # reward for surviving longer than an opponent (awarded when opponent dies)

        # Debug flags
        self.run_until_last_player_dies = run_until_last_player_dies
        self.ignore_self_collisions = ignore_self_collisions

        # Diagnostics
        self.timing_stats = []

        colorama.init()

        # Spawn GUI unless in headless mode
        if self.mode == 'headless':
            self.fps_locked = False
            self.gui = None
        else:
            from gui import AchtungDieKurveGUI
            # Enable GUI. Spawn game window
            self.fps_locked = True
            self.gui = AchtungDieKurveGUI(self)


    def _roll_random_angle(self):
        return 2*pi*self.rng.random()

    def _roll_valid_start_position(self, max_attempts=100):
        attempt_counter = 0
        while attempt_counter < max_attempts:
            x = self.min_turn_radius + (self.screen_width - 2 * self.min_turn_radius) * self.rng.random()
            y = self.min_turn_radius + (self.screen_height - 2 * self.min_turn_radius) * self.rng.random()

            for p in self.players:
                dist = sqrt((x - p.pos[0])**2 + (y - p.pos[1])**2)
                if dist < self.spawn_safety_distance:
                    logging.debug("re-rolling start position")
                    break
            else:
                return x,y

            attempt_counter += 1

        raise RuntimeError("Unable to generate valid start position!")

    @property
    def gui_enabled(self):
        return self.gui is not None

    def detect_wall_collision(self, player:Player):
        x,y = player.pos
        return x < self.game_bounds[0] or x > self.game_bounds[1] or y < self.game_bounds[2] or y > self.game_bounds[3]

    def roll_player_seed(self):
        return self.rng.integers(0,100000)

    def spawn_player(self, idx, init_pos=None, init_angle=None, player_type=Player, **kwargs):
        assert idx in self.valid_player_ids

        if idx in [p.idx for p in self.players]:
            raise ValueError(f"Player {idx} already exists")

        if init_pos is None:
            init_pos = self._roll_valid_start_position()

        if init_angle is None:
            init_angle = self._roll_random_angle()

        if self.rng_seed is not None:
            player_seed = self.roll_player_seed()
        else:
            player_seed = None

        player_kwargs = dict(idx=idx, init_pos=init_pos, init_angle=init_angle,
                             dist_per_tick=self.dist_per_tick,
                             dphi_per_tick=self.dphi_per_tick,
                             color_name=self.player_color_names[idx],
                             radius=self.player_radius,
                             rng_seed=player_seed
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

        if self.gui_enabled:
            # Attach actor to player
            if isinstance(p, NStepPlanPlayer):
                from adp_game.actors import NStepPlanPlayerActor
                p.actor = NStepPlanPlayerActor(p)
            else:
                from adp_game.actors import PlayerActor
                p.actor = PlayerActor(p)

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


    # def draw_start_positions(self):
    #     for p in self.active_players:
    #         p.draw(self.screen)
    #
    #     pygame.display.flip()


    def move_players(self, actions, draw=True, draw_debug=False):
        """ Advance players by one tick/frame

        Returns: timing information
        """
        # Refill screen to remove old player/enemy positions
        # screen.fill((0,0,0))

        timing = {'coll_checks':0., 'draw':0., 'draw_dbg':0.}

        # NOTE: parallelize this?
        for p in self.active_players:
            # Process player input
            p.apply_steering(actions[p.idx])
            # Update player positions
            p.move()
            # Draw player at its current position
            if draw:
                t0 = time.time()
                p.draw(self.gui.screen)
                timing['draw'] += time.time() - t0
            if draw_debug:
                t0 = time.time()
                p.draw_debug_info(self.gui.screen)
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
        with open(fp, "wb") as f:
            pickle.dump(game_state, f)


    def tick_forward(self):
        """
        Advance game state by one tick

        Return timing info
        """
        self.current_frame += 1
        logging.debug(f">==== Frame {self.current_frame:d} ===============")

        actions = defaultdict(lambda: PlayerAction.KeepStraight)

        # Get inputs from human players from GUI
        if self.gui_enabled:
            human_actions = self.gui.query_human_player_actions()
            actions.update(human_actions)

        # Query AI-players for steering actions
        t0_ai = time.time()
        game_state = self.get_game_state()
        for ap in self.active_players:
            if isinstance(ap, AIPlayer):
                actions[ap.idx] = ap.next_action(game_state=game_state)

        dt_ai = time.time() - t0_ai

        for sp in self.active_players:
            if isinstance(sp, ScriptedPlayer):
                actions[sp.idx] = sp.query_steering()


        if self.mode == "gui":
            timing = self.move_players(actions, draw=True, draw_debug=False)
        elif self.mode == "gui-debug":
            timing = self.move_players(actions, draw=True, draw_debug=True)
        else:
            timing = self.move_players(actions, draw=False, draw_debug=False)

        timing['ai'] = dt_ai

        if len(self.active_players) == 1:
            self.winner = self.active_players[0]
            if not self.run_until_last_player_dies:
                self.running = False

        elif len(self.active_players) == 0:
            self.running = False

        return timing


    def reverse_tick(self):
        """Step back game by 1 tick"""

        for p in self.players:
            p.undo_last_move()


    def run_game_loop(self):
        if self.gui_enabled:
            self.gui.run_game_loop()
        else:
            self.run_headless_game_loop()


    def run_headless_game_loop(self):
        # Variable to keep the main loop running
        self.running = True
        closed_by_user = False
        # Main game loop
        while self.running:
            ft_t0 = time.time()  # frame time timer
            timing = {}

            if self.paused:
                # avoid looping too fast while paused
                time.sleep(1/self.target_fps)
                continue

            if closed_by_user:
                logging.info("Game was stopped by user")
                self.running = False
                self.quit()

            # Advance game state by one tick
            tf_timing = self.tick_forward()
            timing.update(tf_timing)

            timing['frame_time'] = time.time() - ft_t0
            self.timing_stats.append(timing)


    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            logging.info("Game paused")
        else:
            logging.info("Game continued")


    def scoreboard_as_df(self):
        sb_dict = {}
        for p in self.players:
            sb_dict[p.idx] = {'Name': str(p), 'Score': self.scoreboard[p.idx], 'Distance': p.dist_travelled,
                              'Total Reward': p.total_reward}

        scoreboard = pd.DataFrame.from_dict(sb_dict, orient='index')
        scoreboard.sort_values(by='Score', inplace=True, ascending=False)
        scoreboard = scoreboard.reset_index(drop=True)
        scoreboard.index += 1
        return scoreboard


    def print_scoreboard(self, pretty=True):
        if pretty:
            scoreboard = self.scoreboard_as_df()
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


    def save_state_to_file(self, fp:str):
        data = {'scoreboard': self.scoreboard, 'trails': {p.idx: p.trail for p in self.players}}

        if fp.endswith('.pkl'):
            import pickle as pkl
            with open(fp, 'wb') as f:
                pkl.dump(data, f)

        else:
            raise NotImplementedError()


    def quit(self):
        pass





if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

    game = AchtungDieKurveGame(target_fps=30, game_speed_factor=0.5)
    game.initialize_players([1,2,3,4,5,6])
    game.run_game_loop()

