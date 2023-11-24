from players.player_base import Player

class HumanPlayer(Player):
    def __init__(self, name=None, **player_kwargs):
        super(HumanPlayer, self).__init__(name=name, **player_kwargs)


    def __str__(self):
        return f"Player '{self.name}' ({self.color_name})"
