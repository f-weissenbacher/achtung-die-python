import logging

from players.player_base import Player, PlayerAction

logger = logging.getLogger(__name__)

class ScriptedPlayer(Player):
    def __init__(self, **player_kwargs):
        super().__init__(**player_kwargs)

    def apply_steering(self, pressed_keys):
        # Child classes need to define steering
        pass

    def apply_action(self, action):
        if action == PlayerAction.SteerLeft:
            self.steer_left()
        elif action == PlayerAction.SteerRight:
            self.steer_right()

    def steer_left(self):
        self.angle -= self.dphi_per_tick

    def steer_right(self):
        self.angle += self.dphi_per_tick


class DummyPlayer(ScriptedPlayer):

    def __init__(self, only_log_errors=True, **player_kwargs):
        player_kwargs['idx'] = 0
        if "name" not in player_kwargs or player_kwargs["name"] is None:
            player_kwargs["name"] = "dummy"

        # Call Player constructor
        super().__init__(**player_kwargs)

        if only_log_errors:
            logger.setLevel(logging.ERROR)

    def move(self, log=False):
        super().move(False)


class FixedActionListPlayer(ScriptedPlayer):
    """ Strictly loops through a predefined list of actions (one per tick)."""

    def __init__(self, action_list, **player_kwargs):
        super().__init__(**player_kwargs)

        self.action_list = action_list
        self.list_length = len(action_list)
        self.action_idx = 0

    def apply_steering(self, pressed_keys):
        # Get action from list based on current action_idx
        action = self.action_list[self.action_idx]

        # Perform steering
        self.apply_action(action)

        # Increment action_idx (loop back if necessary!)
        self.action_idx = (self.action_idx + 1) % self.list_length


