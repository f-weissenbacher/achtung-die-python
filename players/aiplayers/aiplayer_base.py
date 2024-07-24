from players.player_base import *


class AIPlayer(Player):
    def __init__(self, game_bounds, **player_kwargs):
        super().__init__(**player_kwargs)

        # bounds of game area [xmin xmax ymin ymax]
        self.xmin, self.xmax, self.ymin, self.ymax = game_bounds

    def __str__(self):
        return f"AIPlayer '{self.name}' ({self.color_name})"

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

        keypresses = {self.steer_left_key: False, self.steer_right_key: False}
        if action == PlayerAction.SteerLeft:
            keypresses[self.steer_left_key] = True
        elif action == PlayerAction.SteerRight:
            keypresses[self.steer_right_key] = True

        return keypresses

    def _pos_inside_bounds(self, pos, border_width=0.0):
        return self.xmin + border_width < pos[0] < self.xmax - border_width and \
               self.ymin + border_width < pos[1] < self.ymax - border_width

    def _dryrun_action(self, action: PlayerAction):
        if action == PlayerAction.SteerLeft:
            new_angle = self.angle - self.dphi_per_tick
        elif action == PlayerAction.SteerRight:
            new_angle = self.angle + self.dphi_per_tick
        else:
            new_angle = self.angle

        return self.pos + self.dist_per_tick * np.array([np.cos(new_angle), np.sin(new_angle)])


