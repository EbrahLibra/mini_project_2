from base_heuristic import BaseHeuristic


class Player:
    HUMAN = 2
    AI = 3

    def __init__(self,
                 nature,
                 depth,
                 heuristic: BaseHeuristic
                 ):
        self.nature = nature
        self.depth = depth
        self.heuristic = heuristic
