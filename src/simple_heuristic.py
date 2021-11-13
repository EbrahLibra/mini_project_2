from random import randint
from base_heuristic import BaseHeuristic


class SimpleHeuristic(BaseHeuristic):

    # We need better solution
    def calculate_value(self, game, max_turn) -> float:
        success_factor = game.winning_line_size
        result = game.is_end()
        if result == 'X':
            return -10000-success_factor
        elif result == 'O':
            return 10000+success_factor
        elif result == '.':
            return 0
        else:
            if max_turn:
                return -(success_factor-1)
            else:
                return success_factor-1


