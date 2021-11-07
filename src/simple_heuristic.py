import random
from base_heuristic import BaseHeuristic


class SimpleHeuristic(BaseHeuristic):

    # We need better solution
    def calculate_value(self, game, max_turn) -> int:
        success_factor = game.winning_line_size
        if max_turn:
            return -(success_factor-1)
        else:
            return success_factor-1
