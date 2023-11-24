from players.player_base import Player

class HumanPlayer(Player):
    def __init__(self, name=None, **player_kwargs):
        self.name = name

        super(HumanPlayer, self).__init__(**player_kwargs)


    def __str__(self):
        return f"Player '{self.name}' ({self.color_name})"
