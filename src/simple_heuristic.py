import random
from base_heuristic import BaseHeuristic


class SimpleHeuristic(BaseHeuristic):
    def __init__(self, max=False):
        self._max = max

    # TODO This function is not working properly
    # We need better solution
    def calculate_value(self, board) -> int:
        board_size = len(board)
        if max:
            return -random.randint(0, board_size - 1)
        else:
            return +random.randint(0, board_size - 1)
