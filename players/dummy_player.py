import logging

from players.player_base import Player, PlayerAction

logger = logging.getLogger(__name__)

class DummyPlayer(Player):

    def __init__(self, only_log_errors=True, **player_kwargs):
        player_kwargs['idx'] = 0
        if "name" not in player_kwargs or player_kwargs["name"] is None:
            player_kwargs["name"] = "dummy"

        # Call Player constructor
        super().__init__(**player_kwargs)

        if only_log_errors:
            logger.setLevel(logging.ERROR)


    def apply_steering(self, pressed_keys):
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


